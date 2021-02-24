import spotipy
from spotipy.oauth2 import SpotifyOAuth
from PlaylistNotFoundException import PlaylistNotFoundException
from db_handler import DBHandler
from youtube import download_to_mp3


def extract_tracks_list(playlist_name: str) -> list:
    scope = 'playlist-read-private'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, redirect_uri='http://localhost/'))

    results = sp.current_user_playlists()
    for i, playlist in enumerate(results['items']):
        songs = []
        if playlist['name'] == playlist_name:
            offset = 0
            pl_id = 'spotify:playlist:' + playlist['id']
            while True:
                response = sp.playlist_items(pl_id,
                                             offset=offset,
                                             fields='items.track.id,total',
                                             additional_types=['track']
                                             )

                if len(response['items']) == 0:
                    break

                songs.extend(response['items'])
                offset = offset + len(response['items'])

            break
    else:
        raise PlaylistNotFoundException(playlist_name)

    song_details = []

    for song in songs:
        song = sp.track(song['track']['id'])
        name = song['name']
        artist = song['artists'][0]['name']

        song_details.append({'name': name, 'artist': artist})

    return song_details

dbh = DBHandler()
# dbh.create_table('test')
print(dbh.check_table_existance('test'))
dbh.insert_record('test', 'artist12', 'name')
dbh.insert_record('test', 'artist123', 'name')
dbh.mark_as_downloaded('test', 2)
print(dbh.find_all_not_downloaded('test'))
download_to_mp3('test', 'mariah carey', 'my all')
