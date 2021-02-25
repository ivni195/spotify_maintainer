#!/usr/bin/python3

import argparse
import os
from db_handler import DBHandler
from api_client import *
from youtube import download_to_mp3

def ask_confirmation() -> bool:
    while True:
        ans = input()
        if ans.lower() not in ['yes', 'no', 'y', 'n']:
            print('Please enter y or n')
        elif ans.lower() in ['yes', 'y']:
            return True
        else:
            return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', help='(update - update the playlist in the local database)\n'
                                       '(download - download all songs marked as not downloaded according to the local database)\n'
                                       '(info - displays info about the given playlist)\n'
                                       '(add-playlist - creates a table in the local database)\n'
                                       '(add-song - manually add a song to the given playlist; must specify -n NAME and -a ARTIST)\n'
                                       '(drop - drops the table with the given name from the local database)',
                        choices=['update', 'download', 'info','add-playlist', 'add-song', 'drop'])
    parser.add_argument('playlist', help='playlist to act on')
    parser.add_argument('-t', '--threads', type=int, help='number of threads used to download songs', default=1)
    parser.add_argument('-n', '--name', help='name of the song - used with "add" option', default=None)
    parser.add_argument('-a', '--artist', help='artist - used with "add" option', default=None)
    parser.add_argument('-c', '--cookie', help='cookie.txt file located in the scripts directory to use when downloading', default=None)
    args = parser.parse_args()

    dbh = DBHandler()

    if args.action == 'add-playlist':
        if dbh.check_table_existance(args.playlist):
            print('This table already exists!')
        else:
            dbh.create_table(args.playlist)
            print(f'Table {args.playlist} succesfully created.')

    if not dbh.check_table_existance(args.playlist):
        print('Playlist not found. Do you want to create it?')
        if ask_confirmation():
            dbh.create_table(args.playlist)
            print(f'Table {args.playlist} succesfully created.')

    if args.action == 'update':
        local = dbh.get_current_songs(args.playlist)
        try:
            remote = extract_tracks_list(args.playlist)
            count = 0
            for song in remote:
                if song not in local:
                    dbh.insert_song(args.playlist, song[0], song[1])
                    count += 1
            print(f'Update finished. Added {count} songs.')

        except PlaylistNotFoundException:
            print('Playlist not found on the spotify user.')
            exit(-1)


    elif args.action == 'download':
        to_download = dbh.find_all_not_downloaded(args.playlist)
        for id, artist, name, _ in to_download:
            download_to_mp3(args.playlist, artist, name, cookies=args.cookie)
            if os.path.isfile(os.path.join(os.path.dirname(__file__), args.playlist, f'{artist} - {name}.mp3')):
                dbh.mark_as_downloaded(args.playlist, id)



    elif args.action == 'info':
        downloaded, total = dbh.get_table_info(args.playlist)
        print(f'Playlist {args.playlist}:\n{downloaded}/{total} songs already downloaded.')

    elif args.action == 'add-song':
        if args.artist == None or args.name == None:
            print('Please specify artist and name with "-a ARTIST -n NAME"')
        else:
            if dbh.search_song(args.playlist, args.artist, args.name):
                print('This song is already in the playlist. Do you want to add duplicate?')
                if ask_confirmation():
                    dbh.insert_song(args.playlist, args.artist, args.name)
            else:
                dbh.insert_song(args.playlist, args.artist, args.name)


    elif args.action == 'drop':
        print(f'Are you sure you want to delete {args.playlist}?')
        if ask_confirmation():
            pass
#         TODO


    dbh.commit()
