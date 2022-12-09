import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import os
from dotenv import load_dotenv

#import env variables
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

client_credentials_manager = SpotifyClientCredentials(client_id = CLIENT_ID, 
                                                    client_secret = CLIENT_SECRET)

sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)


master_playlist = []
playlists = []
playlists_full_data = []
num_playlist = 0
continue_var = 'Yes'

#loop to add desired number fo playlists
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

    simple_song_data_for_my_playlist = total_playlist_data[["song_name", 
                                                                    "artist", 
                                                                    "genre", 
                                                                    "popularity", 
                                                                    "danceability", 
                                                                    "tempo"]]

    #print(simple_song_data_for_my_playlist)
    playlists.append(simple_song_data_for_my_playlist)
    playlists_full_data.append(total_playlist_data)
    #print(playlists[num_playlist])

    num_playlist = num_playlist + 1
    continue_var = input("Continue (Yes or No): ")


#Reverses playlist to match the order they were entered in 
playlists.reverse()
num_playlist = num_playlist - 1

#Combines all playlists into one while removing duplicates
master_playlist = pd.concat(playlists).drop_duplicates().reset_index(drop=True)

print(playlists_full_data)
print(master_playlist)


#averages advanced numeric data for all playlists 
'''count = 0
col_labels = []
for playlists in playlists_full_data:
    col_count = 0
    for item in playlists_full_data[count]:
        if playlists_full_data[count][item].dtypes == 'float64' or playlists_full_data[count][item].dtypes ==  'int64':
            col_labels = list(playlists_full_data[count].columns)
            #cols = list(simple_song_data_for_my_playlist.columns)
            #print(cols[cols_count]," - ",simple_song_data_for_my_playlist[item][count])
            print(col_labels[col_count], ": ", round(playlists_full_data[count][item].mean(), 2))
        col_count = col_count + 1
    count = count + 1'''



#Finds average, maximum, and miniumum values in playlists
count = 0
col_labels = []
for playlists in playlists_full_data:
    col_count = 0
    for item in playlists_full_data[count]:
        if playlists_full_data[count][item].dtypes == 'float64' or playlists_full_data[count][item].dtypes ==  'int64':
            col_labels = list(playlists_full_data[count].columns)
            print(col_labels[col_count].capitalize(),": ")
            print("\tAverage: ", round(playlists_full_data[count][item].mean(), 2))
            song = playlists_full_data[count]['song_name'].loc[playlists_full_data[count][item] == playlists_full_data[count][item].max()].values[0]
            print("\tMaximum: ", song ,round(playlists_full_data[count][item].max(), 2))
            #print(playlists_full_data[count]['song_name'].loc[playlists_full_data[count][item] == playlists_full_data[count][item].max()])
            #playlists_full_data[count].query(playlists_full_data[count][item] == playlists_full_data[count][item].max())
            print("\tMinimum: ", round(playlists_full_data[count][item].min(), 2))
        col_count = col_count + 1
    count = count + 1


#print(playlists_full_data[count]['song_name'].itemsloc[playlists_full_data[count][item] == playlists_full_data[count][item].max()])
#prints out playlists
'''
while num_playlist >= 0:
    #print(playlists[num_playlist])
    num_playlist = num_playlist- 1

'''

#search for song data
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


'''
#average popularity
total_popularity = 0
count = 0 

for song in simple_song_data_for_my_playlist:
  total_popularity = total_popularity + simple_song_data_for_my_playlist["popularity"][count]
  count = count + 1

average_popularity = total_popularity/count

#average danceability
total_danceability = 0.0
count = 0.0 

for song in simple_song_data_for_my_playlist:
  total_danceability = total_danceability + simple_song_data_for_my_playlist["danceability"][count]
  count = count + 1.0


average_danceability = total_danceability/count

print('Average Popularity:', int(average_popularity))
print('Average Danceability:', round(average_danceability,2))


print(detailed_song_features)

'''