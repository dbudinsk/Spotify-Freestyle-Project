import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd


client_credentials_manager = SpotifyClientCredentials(client_id = '9ea63cfe9be44a5abe89e5cdcaa077da', 
                                                    client_secret = '13f762e20e9240319f71faed2f68e886')

sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)


playlists = []
playlists__full_data = []
num_playlist = 0
continue_var = 'Yes'

while continue_var != "No":
    playlist = input("Enter a playlist Share URL: ")

    playlist_link = playlist
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]
    track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]

    tracks_in_my_playlist_info = sp.playlist_tracks(playlist_URI)

    uri = []
    name = []
    artist = []
    artist_main_genre = []
    popularity = []


    for entry in tracks_in_my_playlist_info["items"]:

        uri.append(entry["track"]["uri"].split(":")[-1])
        name.append(entry["track"]["name"])
        artist.append(entry["track"]["artists"][0]["name"])
        try:
            artist_main_genre.append(sp.artist(entry["track"]["artists"][0]["uri"])["genres"][0])
        #genre is set to unknown if it's missing in a song 
        except IndexError:
            artist_main_genre.append("unknown")

        popularity.append(entry["track"]["popularity"])


    song_data = pd.DataFrame({'song_uri': uri,
                                    'song_name': name,
                                    'artist': artist,
                                    'genre' : artist_main_genre,
                                    'popularity': popularity})


    detailed_song_features = sp.audio_features(song_data['song_uri'])
    detailed_song_features = pd.DataFrame.from_dict(detailed_song_features)


    total_playlist_data = pd.merge(left = song_data, 
                                            right = detailed_song_features, 
                                            left_on = "song_uri", 
                                            right_on= "id")


    print(total_playlist_data)

    simple_song_data_for_my_playlist = total_playlist_data[["song_name", 
                                                                    "artist", 
                                                                    "genre", 
                                                                    "popularity", 
                                                                    "danceability", 
                                                                    "tempo"]]


    print(simple_song_data_for_my_playlist)
    playlists.append(simple_song_data_for_my_playlist)
    playlists__full_data.append(total_playlist_data)
    print(playlists[num_playlist])


    num_playlist = num_playlist + 1

    continue_var = input("Continue (Yes or No): ")



#prints out entered playlist data
playlists.reverse()
num_playlist = num_playlist - 1
while num_playlist >= 0:
    print(playlists[num_playlist])
    num_playlist = num_playlist- 1

'''
    song_to_find = input("Enter a song: ")
    count = 0.0

    cols = []
    cols_count = 0

    for song in simple_song_data_for_my_playlist["song_name"]:
        if song_to_find == simple_song_data_for_my_playlist["song_name"][count]:
            cols = list(simple_song_data_for_my_playlist.columns)
            for item in simple_song_data_for_my_playlist:  
                print(cols[cols_count]," - ",simple_song_data_for_my_playlist[item][count])
                cols_count = cols_count + 1
        
        count = count + 1.0
'''
total_popularity = 0
count = 0 

for song in simple_song_data_for_my_playlist:
  total_popularity = total_popularity + simple_song_data_for_my_playlist["popularity"][count]
  count = count + 1

average_popularity = total_popularity/count


total_danceability = 0.0
count = 0.0 

for song in simple_song_data_for_my_playlist:
  total_danceability = total_danceability + simple_song_data_for_my_playlist["danceability"][count]
  count = count + 1.0


average_danceability = total_danceability/count

print('Average Popularity:', int(average_popularity))
print('Average Danceability:', round(average_danceability,2))


print(detailed_song_features)

