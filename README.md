# Spotify-Freestyle-Project

## Setup

Create and activate a virtual environment:

```sh
conda create -n spotify-freestyle-project python=3.8

conda activate spotify-freestyle-project
```

Install package dependencies:

```sh
pip install -r requirements.txt
```

## Configuration
Obtain necessary credentials from Spotify
https://developer.spotify.com/

create a .env file to store credentials as variables

#.env file
CLIENT_ID: __
CLIENT_SECRET:__

## Usage
first obtain links to spotify playlists to be analyzed
can test with this link: https://open.spotify.com/playlist/37i9dQZF1DXcSC8oOed07w?si=8bc720fc714b4eb9

'''sh
python main_code.py
'''

## Excel/results

After running program, navigate to directory to open file master playlist, summary table, and individual playlists
The song_uri column when pasted into a web address will redirect users to the song on the spotify app

