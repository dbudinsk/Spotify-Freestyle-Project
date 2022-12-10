import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import os
from dotenv import load_dotenv


load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

client_credentials_manager = SpotifyClientCredentials(client_id = CLIENT_ID, 
                                                    client_secret = CLIENT_SECRET)

sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

master_playlist = []
playlists = []
playlists_full_data = []

def get_playlists(num_playlist):
    continue_var = 'Yes'
    while continue_var != "No":
            playlist = input("Enter a playlist Share URL: ")
            if not playlist.startswith("http"):
                print("Error")
                exit()
            playlist_link = playlist
            playlist_URI = playlist_link.split("/")[-1].split("?")[0]
            track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]
            tracks_in_my_playlist_info = sp.playlist_tracks(playlist_URI)
            #create lists to append data
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
                                                                            "tempo",
                                                                            "uri"]]
            #Creates one playlist with basic information
            #Creates one playlist with all information
            playlists.append(simple_song_data_for_my_playlist)
            playlists_full_data.append(total_playlist_data)
            num_playlist = num_playlist + 1
            
            continue_var = input("Continue (Yes or No): ")

    print(num_playlist)
    return num_playlist
            
if __name__ =="__main__":
    num_playlist = 0
    num_playlist=get_playlists(num_playlist)

    print(num_playlist)
    print("test1")

    #Reverses playlist to match the order they were entered in 
    playlists.reverse()
    
    summary_data = pd.DataFrame()
    count = 0
    master_playlist = pd.concat(playlists).drop_duplicates().reset_index(drop=True)
     
    for each_playlist in playlists_full_data:
        col_labels = []
        category = []
        average = []
        maximum = []
        minimum = []
        maxi_song = []
        mini_song = []
        col_count = 0

        for item in playlists_full_data[count]:
            if playlists_full_data[count][item].dtypes == 'float64' or playlists_full_data[count][item].dtypes ==  'int64':
                col_labels = list(playlists_full_data[count].columns)
                category.append(col_labels[col_count])

                average.append(round(playlists_full_data[count][item].mean(), 2))
                
                max_song = playlists_full_data[count]['song_name'].loc[playlists_full_data[count][item] == playlists_full_data[count][item].max()].values[0]
                maximum.append(round(playlists_full_data[count][item].max(), 2))
                maxi_song.append(max_song)
            
                min_song = playlists_full_data[count]['song_name'].loc[playlists_full_data[count][item] == playlists_full_data[count][item].min()].values[0]
                minimum.append(round(playlists_full_data[count][item].min(), 2))
                mini_song.append(min_song)

            col_count = col_count + 1
    
        temp_data = pd.DataFrame({'Category': category,
                                        'Average':average , 
                                        'Maximum': maximum ,
                                        'Max_Song': maxi_song,
                                        'Minimum': minimum ,
                                        'Min_Song': mini_song})
        count = count + 1
        summary_data = summary_data.append(temp_data)
    

    playlist_label = "Playlist"
    with pd.ExcelWriter("Playlist Summary.xlsx") as writer:
        master_playlist.to_excel(writer, sheet_name= "Master Playlist")
        summary_data.to_excel(writer, sheet_name= "Summary")
        count = 0
        while count < num_playlist:
            playlists[count].to_excel(writer, sheet_name= (playlist_label + str(count+1)))
            count = count + 1

    #Combines all playlists into one while removing duplicates
    print(playlists)
   