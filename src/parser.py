import markdown
import os
import yaml
from markdown.extensions import Extension
from markdown.postprocessors import Postprocessor
import re

# Read the config
with open('config.yaml', 'r') as f:
    config_data = yaml.load(f, Loader=yaml.SafeLoader)
MD_PATH = config_data.get("MD_PATH")

# Custom MD
class CodeTagExtension(Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.postprocessors.register(CodeTagPostprocessor(md), 'codetag', 175)

class CodeTagPostprocessor(Postprocessor):
    def run(self, text):
        # Regex to find the pattern [string]
        pattern = re.compile(r'\[(.+?)\]')
        # Replace with <code>string</code>
        return re.sub(pattern, r'<code>\1</code>', text)

def make_extension(**kwargs):
    return CodeTagExtension(**kwargs)






class Song:
    def __init__(self, name: str, artist: str, tune: str, song_html: str):
        self.name = name
        self.artist = artist
        self.tune = tune
        self.song_html = song_html


# Transform from name of md file to title
def name_to_title(name):
    return name.replace("_", " ").replace("-", " - ").title()

# Returns the list of songs
def get_songs_list():
    songs_list = os.listdir(MD_PATH)
    for i, song in enumerate(songs_list):
        songs_list[i] = song.removesuffix(".md")
    return songs_list

    
def md_to_html(md_song) -> str:
    html_text = markdown.markdown(md_song, xtensions=[CodeTagExtension()])
    # Leave spaces
    html_text = "<pre>\n" + html_text.replace("<pre>", "").replace("</pre>", "") + "\n</pre>"

    return html_text


# Gets the info with the field target_text
def get_info_header(header_text: str, target_text: str) -> str:
    title_line = [line for line in header_text.split('\n') if target_text + ": " in line][0]
    return title_line.replace(target_text + ": ", "")


def md_to_Song(song: str) -> Song:
    file_md_path = MD_PATH + song + ".md"
    with open(file_md_path, 'r') as f:
        md_text = f.read()

    [md_header, md_song] = md_text.split("---")

    name = get_info_header(md_header, "Name")
    artist = get_info_header(md_header, "Artist")
    tune = get_info_header(md_header, "Tune")

    return Song(name = name, artist = artist, tune = tune, song_html = md_to_html(md_song))


# Test
"""
s = md_to_Song("wonderwall")
print(s.name)
print(s.artist)
print(s.tune)
print(s.song_html)
"""
s = md_to_Song("stick_season-noah_kahan")
print(s.song_html)