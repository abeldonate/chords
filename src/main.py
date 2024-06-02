import os
import datetime
from flask import Flask, render_template, url_for
from parser import md_to_Song, get_songs_list, name_to_title

template_path = os.path.abspath("src/templates")
static_path = os.path.abspath("src/static")

app = Flask(
    __name__,
    template_folder=template_path,
    static_folder=static_path,
)


@app.route('/')
def page_index():
    return render_template('index.html', songs_list = get_songs_list(), name_to_title = name_to_title)


@app.route('/<song>')
def page_song(song):
    return render_template('song.html', song = md_to_Song(song))

if __name__ == '__main__':
    app.run()
