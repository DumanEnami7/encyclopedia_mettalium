# library imports
from flask import Flask, render_template, jsonify, request, flash # type: ignore
from livereload import Server # type: ignore
from helpers import search_song
# create flask app
app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    if request.method =="GET":
        return render_template("index.html", genres=[], band_image=None, spotify_url=None)
    
@app.route("/search", methods=["POST"])
# searching a band
def search():
    user_input = request.form.get("band_name")
    # empty input corner case
    if user_input == "":
        return render_template("index.html")
    
    # search the song from the helper file
    band_info, album_info = search_song(user_input)
    if band_info == False:
        return render_template("error.html",msg="song not found")
    # return given results
    return render_template(
        "index.html", band_image = band_info["band_image"],spotify_url = band_info["spotify_url"],genres=band_info["genres"], listeners = band_info["listeners"],band_name = band_info["band_name"],
        album_names = album_info["album_names"],album_links=album_info["album_links"],album_track_num=album_info["album_track_number"],album_img=album_info["album_images"],
        album_dates = album_info["album_dates"]
        )

if __name__ == '__main__':
    app.run(debug=True)
