import youtube_dl
import os
import threading
import re
from math import ceil

curr_dir = os.path.dirname(__file__)


class DownloadSession:
    def __init__(self, n_threads: int, playlist_name: str, song_list: list, cookies=None):
        self.n_threads = n_threads
        self.lock = threading.Lock()
        self.total = len(song_list)
        self.successful = 0
        self.failed = 0
        self.song_list: list = song_list
        self.playlist: str = playlist_name
        self.downloaded = []
        self.cookies: str = cookies

    def _download(self, playlist: str, song: tuple):
        """
        Download a song.
        If successfull, increment self.successful and append song's id to self.downloaded.
        Else, increment self.failed.
        :song should be a tuple of a form (id, artist, name, downloaded_flag)
        """
        idx, artist, name, _ = song
        regex = r'[$&+,:;=?@#|/\'<>.^*()%!-]'
        artist = re.sub(regex, '', artist)
        name = re.sub(regex, '', name)

        # if playlist directory doesn't exist, create it
        try:
            os.makedirs(os.path.join(curr_dir, playlist))
        except:
            pass

        opts = {
            'default_search': 'auto',
            'outtmpl': os.path.join(curr_dir, playlist, f'{artist} - {name}.webm'),
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '96',
            }],
            'quiet': True
        }
        # set the cookies.txt location if specified
        if self.cookies is not None:
            opts['cookiefile'] = self.cookies

        # actually download the song
        with youtube_dl.YoutubeDL(opts) as ydl:
            try:
                ydl.download([artist + name])
            except:
                pass

        # if the file is there, it means success
        if os.path.isfile(os.path.join(os.path.dirname(__file__), self.playlist, f'{artist} - {name}.mp3')):
            self.downloaded.append(idx)
            # use thread lock to avoid race conditions
            with self.lock:
                self.successful += 1
            print(f'Downloaded {artist} - {name} [{self.successful}/{self.total}]')
        else:
            with self.lock:
                self.failed += 1

    def _download_chunk(self, chunk: list):
        """
        Download all songs from chunk.
        This method is meant to be run in a seperate thread every time when called.
        """
        if len(chunk) > 0:
            for song in chunk:
                self._download(self.playlist, song)

    def start(self) -> list:
        """
        Start the multithreaded download.
        :return: list of successfully downloaded songs
        """
        chunk_size = ceil(self.total / self.n_threads)
        chunks = [self.song_list[i:i + chunk_size] for i in range(0, len(self.song_list), chunk_size)]

        threads = []
        for i in range(len(chunks)):
            x = threading.Thread(target=self._download_chunk, args=(chunks[i],))
            threads.append(x)
            x.start()
            print(f'Starting thread {i}.')

        for thread in threads:
            thread.join()

        print(f'Downloaded succesfully {self.successful} song, {self.failed} failed.')
        return self.downloaded
