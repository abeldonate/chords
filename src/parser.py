import os
import yaml
import re

# Read the config
with open('config.yaml', 'r') as f:
    config_data = yaml.load(f, Loader=yaml.SafeLoader)

MD_PATH = config_data.get("MD_PATH")
CHORD_OPEN = config_data.get("CHORD_OPEN")
CHORD_CLOSE = config_data.get("CHORD_CLOSE")
LETTERS = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]


class Song:
    def __init__(self, filename: str, name: str, artist: str, tune: str, song_html: str):
        self.filename = filename
        self.name = name
        self.artist = artist
        self.tune = tune
        self.song_html = song_html


# Transform from name of md file to title
"""
def name_to_title(name):
    return name.replace("_", " ").replace("-", " - ").title()
"""

# Returns the list of songs
def get_songs_list():
    songs_list = os.listdir(MD_PATH)
    for i, song in enumerate(songs_list):
        songs_list[i] = song.removesuffix(".md")
    return songs_list

    
def md_to_html(md_song) -> str:
    # Parse <Chord>
    pattern = rf'{CHORD_OPEN}(.*?){CHORD_CLOSE}'
    html_text = re.sub(pattern, lambda match: f'<code>{match.group(1)}</code>', md_song)

    # Leave spaces
    html_text = "<pre>\n" + html_text + "\n</pre>"

    return html_text


# Gets the info with the field target_text
def get_info_header(header_text: str, target_text: str) -> str:
    title_line = [line for line in header_text.split('\n') if target_text + ": " in line][0]
    return title_line.replace(target_text + ": ", "")

def flat_to_sharp(chord):
    if chord == "Ab": return "G#"
    if chord == "Bb": return "A#"
    if chord == "Db": return "C#"
    if chord == "Eb": return "D#"
    if chord == "Gb": return "F#"

def transport_chord(chord: str, tune: int):
    if len(chord) == 1:
        return LETTERS[ (LETTERS.index(chord) + tune) % 12]
    elif chord[1] == "#":
        let = chord[0:2]
        return chord.replace(let, LETTERS[ (LETTERS.index(let) + tune) % 12])
    elif chord[1] == "b":
        let = flat_to_sharp(chord[0:2])
        return chord.replace(let, LETTERS[ (LETTERS.index(let) + tune) % 12])
    let = chord[0]
    return chord.replace(let, LETTERS[ (LETTERS.index(let) + tune) % 12])
    

#Transports html to a target relative tune (in semitones)
def transport_song(text: str, tune: int): 
    pattern = r'<code>(.*?)</code>'
    
    # Use re.sub with a lambda function to apply the transformation
    result = re.sub(pattern, lambda match: f'<code>{transport_chord(match.group(1), tune)}</code>', text)
    
    return result


def md_to_Song(song: str, newtune: int) -> Song:
    file_md_path = MD_PATH + song + ".md"
    with open(file_md_path, 'r') as f:
        md_text = f.read()

    [md_header, md_song] = md_text.split("---")

    filename = song
    name = get_info_header(md_header, "Name")
    artist = get_info_header(md_header, "Artist")
    #tune = get_info_header(md_header, "Tune")
    song_html = transport_song(md_to_html(md_song), newtune)

    return Song(filename = filename, name = name, artist = artist, tune = newtune, song_html = song_html)


def sum_tunes(t1, t2):
    return t1+t2

# Test
#s = md_to_Song("no_ho_entens-els_amics_de_les_arts")
#print(s.filename)