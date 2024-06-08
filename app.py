import streamlit as st
import pickle
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


CLIENT_ID = "25d2dc22ee0745f98bf3c9ef9c856a3b"
CLIENT_SECRET = "c12742104b8441118faaa0443c341736"

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)



st.title('Song Recommender System')

def song_cover(song_name,artist_name):
   search_query= f"track:{song_name} artist:{artist_name}"
   results = sp.search(q=search_query,type="track")

   if results and results["tracks"]["items"]:
      track = results["tracks"]["items"][0]
      cover_url = track["album"]["images"][0]["url"]
      return cover_url
   else:
      return "http://i.postimg.cc/0QNxYz4V/social.png"

def recommend(selected_song):
   index = songs[songs['track_name'] == selected_song].index[0]
   distances = similarity[index]
   song_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
   recommended_songs = []
   rec_song_cover = []

   for i in song_list:
      singer =songs.iloc[i[0]].artists
      recommended_songs.append(songs.iloc[i[0]].track_name)
      rec_song_cover.append(song_cover(songs.iloc[i[0]].track_name,singer))
   return recommended_songs, rec_song_cover


song_dict = pickle.load(open('song_dict2.pkl','rb'))
songs = pd.DataFrame(song_dict)
similarity = pickle.load(open('similarity2.pkl','rb'))
selected_song = st.selectbox(
   "Your favorite song",
   songs['track_name'].values,
   index=None,
   placeholder="Select song",
)

if st.button('Recommend'):
   recommendations, poster = recommend(selected_song)
   col1,col2,col3,col4,col5 = st.columns(5)
   with col1:
      st.text(recommendations[0])
      st.image(poster[0])
   with col2:
      st.text(recommendations[1])
      st.image(poster[1])
   with col3:
      st.text(recommendations[2])
      st.image(poster[2])
   with col4:
      st.text(recommendations[3])
      st.image(poster[3])
   with col5:
      st.text(recommendations[4])
      st.image(poster[4])


