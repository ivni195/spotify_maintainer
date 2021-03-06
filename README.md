# spotify_maintainer
## Description
Spotify_mainteiner is a script written 
in Python that lets you fetch playlists 
from your Spotify account and download them as mp3 files.
It creates local database that stores information about which
song has already been downloaded so that when you update your 
Spotify playlist, it will download only newly added songs.

## Prerequisites
The script uses youtube-dl and spotipy. Download
them using pip.

`pip3 install youtube-dl spotipy`

In addition `ffmpeg` is requiered. Install it by adding 
its location to `PATH`.

## Install
Simply download using git

`git clone https://github.com/ivni195/spotify_maintainer`

You also need to set up `SPOTIPY_CLIENT_ID` and `SPOTIPY_CLIENT_SECRET`
enviroment variables which you can obtain via Spotify developer panel.

## Usage
You should run the script directly from the script directory. 
When you want to download playlist 'example_playlist' from Spotify,
first you need to add it to the local database.

`python3 spfmaint.py add-playlist example_playlist`

Now download playlist info from Spotify API. (Note that if you skip
the first step, you will be prompted to create the table.) When you do it
for the first time, your web browser will pop up and you will be ask to paste
in the redirect link (this is how spotipy authenticates a user). 

`python3 spfmaint.py update example_playlist`

Finally, download the songs. A new directory named 'example_playlist'
will be created. This is where all downloaded songs will be stored.

`python3 spfmaint.py download example_playlist`