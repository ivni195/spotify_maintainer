#!/usr/bin/python3

import argparse
from db_handler import DBHandler
from api_client import *

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
    args = parser.parse_args()

    dbh = DBHandler()

    dbh.insert_record('test', 'artist12', 'name')
    dbh.insert_record('test', 'artist12', 'name')
    dbh.insert_record('test', 'artist123', 'name')
    dbh.mark_as_downloaded('test', 2)

    if args.action == 'add-playlist':
        if dbh.check_table_existance(args.playlist):
            print('This table already exists!')
        else:
            dbh.create_table(args.playlist)
            print(f'Table {args.playlist} succesfully created.')

    if not dbh.check_table_existance(args.playlist):
        print('Playlist not found.')

    if args.action == 'update':
        local = dbh.get_current_songs(args.playlist)
        remote = extract_tracks_list(args.playlist)
        count = 0
        for song in remote:
            if song not in local:
                dbh.insert_record(args.playlist, song[0], song[1])
                count += 1
        print(f'Update finished. Added {count} songs.')

    elif args.action == 'download':
        pass

    elif args.action == 'info':
        downloaded, total = dbh.get_table_info(args.playlist)
        print(f'Playlist {args.playlist}:\n{downloaded}/{total} songs already downloaded.')



    elif args.action == 'add-song':
        pass

    elif args.action == 'drop':
        pass

