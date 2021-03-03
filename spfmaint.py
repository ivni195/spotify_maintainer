#!/usr/bin/python3

"""
Spotify_maintainer is a script written
in Python that lets you fetch playlists
from your Spotify account and download them as mp3 files.
It creates local database that stores information about which
song has already been downloaded so that when you update your
Spotify playlist, it will download only newly added songs.
"""

import argparse
from db_handler import DBHandler
from api_client import *
from youtube import DownloadSession


def ask_confirmation() -> bool:
    """
    basic prompt for comfirmation
    :return: True if user comfirmed, False otherwise
    """
    while True:
        ans = input()
        if ans.lower() not in ['yes', 'no', 'y', 'n']:
            print('Please enter y or n')
        elif ans.lower() in ['yes', 'y']:
            return True
        else:
            return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    # positional arguments
    parser.add_argument('action', help='update - update the playlist in the local database\n'
                                       'download - download all songs marked as not downloaded according to the local database\n'
                                       'info - displays info about the given playlist\n'
                                       'add-playlist - creates a table in the local database\n'
                                       'add-song - manually add a song to the given playlist; must specify -n NAME and -a ARTIST\n'
                                       'clear - clears the table with the given name',
                        choices=['update', 'download', 'info', 'add-playlist', 'add-song', 'clear'])
    parser.add_argument('playlist', help='playlist to act on', default=None)

    # optional arguments
    parser.add_argument('-t', '--threads', type=int,
                        help='number of concurent threads used to download songs (4 by default)', default=4)
    parser.add_argument('-n', '--name', help='name of the song - used with "add" option', default=None)
    parser.add_argument('-a', '--artist', help='artist - used with "add" option', default=None)
    parser.add_argument('-c', '--cookies',
                        help='cookie.txt file located in the scripts directory to use when downloading', default=None)
    args = parser.parse_args()

    # open database
    dbh = DBHandler()

    # create a a table if it doesn't exist
    if args.action == 'add-playlist':
        if dbh.check_table_existance(args.playlist):
            print('This table already exists!')
        else:
            dbh.create_table(args.playlist)
            print(f'Table {args.playlist} succesfully created.')

    # if acting on a nonexistent table, prompt the user to create it
    if not dbh.check_table_existance(args.playlist):
        print('Playlist not found. Do you want to create it?')
        if ask_confirmation():
            dbh.create_table(args.playlist)
            print(f'Table {args.playlist} succesfully created.')

    # download track list from spotify
    if args.action == 'update':
        local = dbh.get_all_songs(args.playlist)
        try:
            remote = extract_tracks_list(args.playlist)
            count = 0
            # only add songs that hasn't been already added
            for song in remote:
                if song not in local:
                    dbh.insert_song(args.playlist, song[0], song[1])
                    count += 1
            print(f'Update finished. Added {count} songs.')

        except PlaylistNotFoundException:
            print('Playlist not found on the spotify user.')
            exit(-1)

    # download songs marked as not downloaded
    elif args.action == 'download':
        to_download = dbh.get_all_not_downloaded(args.playlist)
        ds = DownloadSession(args.threads, args.playlist, to_download, args.cookies)

        if len(to_download) > 0:
            downloaded = ds.start()
            for i in downloaded:
                dbh.mark_as_downloaded(args.playlist, i)
        else:
            print('No more songs to download.')

    # display info about playlist
    elif args.action == 'info':
        downloaded, total = dbh.get_table_info(args.playlist)
        print(f'Playlist {args.playlist}:\n{downloaded}/{total} songs already downloaded.')

    # manually add a song to a playlist by specyfying -a and -n
    elif args.action == 'add-song':
        if args.artist == None or args.name == None:
            print('Please specify artist and name with "-a ARTIST -n NAME"')
        else:
            # ask whether to add duplicate
            if dbh.search_song(args.playlist, args.artist, args.name):
                print('This song is already in the playlist. Do you want to add duplicate?')
                if ask_confirmation():
                    dbh.insert_song(args.playlist, args.artist, args.name)
            else:
                dbh.insert_song(args.playlist, args.artist, args.name)

    # clear the local database
    elif args.action == 'clear':
        print(f'Are you sure you want to clear {args.playlist}?')
        if ask_confirmation():
            dbh.clear_table(args.playlist)
            print(f'Table {args.playlist} has been cleared.')

    # commit changes to the database
    dbh.commit()
    print('Database updated.')
