class PlaylistNotFoundException(Exception):
    def __init__(self, playlist_name):
        super().__init__(f'{playlist_name}: no such playlist.')
