from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy import *


clientID = "YOUR CLIENT ID FROM SPOTIFY"
client_secret = "YOUR CLIENT SECRET FROM SPOTIFY"

year = input("Which year do you want to travel to? Type the date in this format: YYYY-MM-DD: ")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{year}")
billboard_site = response.text

soup = BeautifulSoup(billboard_site, "html.parser")

titles = soup.select("li ul li h3")
top_100_list = [title.getText().strip() for title in titles]
print(top_100_list)


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=clientID,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt",
        username="YOUR SPOTIFY USERNAME",
    )
)

user_id = sp.current_user()["id"]

song_uris = []
your_year = year.split("-")[0]

for song in top_100_list:
    result = sp.search(f"track:{song} year:{your_year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify, Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{year} Billboard 100", public=False)
print(playlist["id"])

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)







