import spotipy
from spotipy.oauth2 import SpotifyOAuth
from PlaylistNotFoundException import PlaylistNotFoundException

def extract_tracks_list(playlist_name: str) -> list:
    scope = 'playlist-read-private'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, redirect_uri='http://localhost/'))

    results = sp.current_user_playlists()
    for playlist in results['items']:
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

        song_details.append((artist, name))

    return song_details