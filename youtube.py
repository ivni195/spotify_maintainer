import youtube_dl
import os

curr_dir = os.path.dirname(__file__)


class Song:
    def __init__(self, url, title, duration):
        self.url = url
        self.title = title
        self.duration = duration


def fetch_songs_info(query):
    opts = {
        'default_search': 'auto',
        'simulate': True,
        'ignoreerrors': True,
        'quiet': True
        # 'cookiefile': os.path.join(curr_dir, 'cookies.txt')
    }

    with youtube_dl.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(query)

    songs = []

    if '_type' in info.keys() and info['_type'] == 'playlist':
        for entry in info['entries']:
            if entry:
                url = entry['webpage_url']
                title = entry['title']
                duration = entry['duration']
                songs.append(Song(url, title, duration))
    else:
        url = info['webpage_url']
        title = info['title']
        duration = info['duration']
        songs.append(Song(url, title, duration))

    return songs


def download_to_mp3(playlist, artist, name, cookies=None):
    if not os.path.exists(os.path.join(curr_dir, playlist)):
        os.makedirs(os.path.join(curr_dir, playlist))

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
    if cookies is not None:
        opts['cookiefile'] = os.path.join(curr_dir, 'cookies.txt'),

    with youtube_dl.YoutubeDL(opts) as ydl:
        try:
            ydl.download([artist + name])
        except:
            pass


