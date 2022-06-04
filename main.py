import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from bs4 import BeautifulSoup

date = input("Which year do you travel? type the data in this format YYYY-MM-DD:")
response = requests.get("https://www.billboard.com/charts/hot-100/" + date)
data = response.text
soup = BeautifulSoup(data, "html.parser")
song_names = soup.find_all(name="h3", class_="c-title")
song_title = [song.getText().strip() for song in song_names]


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com/callback/",
        client_id="81b0ff4843d8402a9ca1f035ccae7f56",
        client_secret="a5cf0c6ce5d44c119757dd4dcfef9e68",
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
print(user_id)

song_names = ["The list of song", "titles from your", "web scrape"]


song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exit in spotify. skipped")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
