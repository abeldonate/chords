import os
import datetime
from flask import Flask, render_template, url_for
from parser import md_to_Song, get_songs_list, sum_tunes, to_spaces, to_underscore

template_path = os.path.abspath("src/templates")
static_path = os.path.abspath("src/static")

app = Flask(
    __name__,
    template_folder=template_path,
    static_folder=static_path,
)


@app.route('/')
def page_index():
    return render_template('index.html', songs_list = get_songs_list(), md_to_Song = md_to_Song, to_underscore = to_underscore)

@app.route('/<artist>')
def page_artist(artist):
    return render_template('artist.html', artist = to_spaces(artist), songs_list = get_songs_list(), md_to_Song = md_to_Song)

@app.route('/<song>/<newtune>')
def page_song(song, newtune):
    return render_template('song.html', song = md_to_Song(song, int(newtune)), newtune = newtune, sum_tunes = sum_tunes)


if __name__ == '__main__':
    app.run()
