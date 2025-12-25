from flask import render_template
from spotipy.oauth2 import SpotifyClientCredentials #type: ignore
import spotipy #type: ignore
import requests

CLIENT_ID = "SERVER API ID ENV"
CLIENT_SECRET = "SERVER API ID ENV"
redirect_url = "http://127.0.0.1:5000/callback"

def search_song(search):
        try:
                # search artist from spotipy API
                sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id = CLIENT_ID, client_secret = CLIENT_SECRET))
                res = sp.search(q=search, type="artist")
                
                # check if the artist exists
                if not res:
                        return False
                
                # get artist ID to search for albums
                artist_id = res["artists"]["items"][0]["id"]
                # search albums
                albums = sp.artist_albums(artist_id, album_type='album')
                # fillings
                albums = albums["items"]
                album_names = []
                album_images = []
                album_links = []
                album_track_number = []
                album_dates = []

                # fill arrays with relevant data from the JSON output
                for album in albums:
                        album.pop("available_markets")
                        album_names.append(album["name"])
                        album_images.append(album["images"][0]["url"])
                        album_links.append(album["artists"][0]["external_urls"]["spotify"])
                        album_dates.append(album["release_date"])
                        album_track_number.append(album["total_tracks"])

                # band URL and image
                url = res["artists"]["items"][0]["external_urls"]["spotify"]
                band_image = res["artists"]["items"][0]["images"][0]["url"]
                listenrs = res["artists"]["items"][0]["followers"]["total"]
                genres = res["artists"]["items"][0]["genres"]
                # pprint(res)
                band_name = res["artists"]["items"][0]["name"]
                print(band_name)
                # checking if an artist has a profile picture
                if not band_image:band_image = None
                # checking if an artist has a genre
                if not genres: genres = None

                # dictionary for the albums
                album_info = {
                        "album_names":album_names,
                        "album_images":album_images,
                        "album_dates":album_dates,
                        "album_track_number":album_track_number,
                        "album_links":album_links
                }

                # dictionary for the band
                band_info = {
                        "band_image":band_image,
                        "spotify_url":url,
                        "genres":genres,
                        "listeners":listenrs,
                        "band_name":band_name
                
                }
                return band_info,album_info
        
        # error handling for timeout errors
        except requests.exceptions.Timeout:
                return render_template("index.html")
