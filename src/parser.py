import os
import yaml
import re

# Read the config
with open('config.yaml', 'r') as f:
    config_data = yaml.load(f, Loader=yaml.SafeLoader)

MD_PATH = config_data.get("MD_PATH")
POSITIONS_PATH = config_data.get("POSITIONS_PATH")
CHORD_MD_OPEN = config_data.get("CHORD_MD_OPEN")
CHORD_MD_CLOSE = config_data.get("CHORD_MD_CLOSE")
CHORD_HTML_OPEN = config_data.get("CHORD_HTML_OPEN")
CHORD_HTML_CLOSE = config_data.get("CHORD_HTML_CLOSE")
KEYS = config_data.get("KEYS")
SEPARATOR = config_data.get("SEPARATOR")

class Song:
    def __init__(self, filename: str, name: str, artist: str, tune: str, header: str, song_html: str):
        self.filename = filename
        self.name = name
        self.artist = artist
        self.tune = tune
        self.header = header
        self.song_html = song_html


def to_spaces(text):
    return text.replace("_"," ").title()

def to_underscore(text):
    return text.replace(" ", "_").lower()


# Returns the list of songs
def get_songs_list():
    songs_list = sorted([f for f in os.listdir(MD_PATH) if os.path.isfile(os.path.join(MD_PATH,f))])
    for i, song in enumerate(songs_list):
        songs_list[i] = song.removesuffix(".md")
    return songs_list


def md_to_html(md_song: str) -> str:
    # Parse <Chord>
    pattern = rf'{CHORD_MD_OPEN}(.*?){CHORD_MD_CLOSE}'
    html_text = re.sub(pattern, lambda match: f'{CHORD_HTML_OPEN}{match.group(1)}{CHORD_HTML_CLOSE}', md_song)

    # Leave spaces
    html_text = "<pre>\n" + html_text + "\n</pre>"

    return html_text


# Gets the info with the field target_text
def get_info_header(header_text: str, target_text: str) -> str:
    title_line = [line for line in header_text.split('\n') if target_text + ": " in line][0]
    return title_line.replace(target_text + ": ", "").title()

def flat_to_sharp(chord: str) -> str:
    if chord == "Ab": return "G#"
    if chord == "Bb": return "A#"
    if chord == "Db": return "C#"
    if chord == "Eb": return "D#"
    if chord == "Gb": return "F#"

def transport_chord(chord: str, tune: int) -> str:
    if len(chord) == 1:
        return KEYS[ (KEYS.index(chord) + tune) % 12]
    elif chord[1] == '#':
        let = chord[0:2]
        return chord.replace(let, KEYS[ (KEYS.index(let) + tune) % 12])
    elif chord[1] == 'b':
        let = flat_to_sharp(chord[0:2])
        return chord.replace(chord[0:2], KEYS[ (KEYS.index(let) + tune) % 12])
    let = chord[0]
    return chord.replace(let, KEYS[ (KEYS.index(let) + tune) % 12])
    

#Transports html to a target relative tune (in semitones)
def transport_song(text: str, tune: int) -> str: 
    pattern = rf'{CHORD_HTML_OPEN}(.*?){CHORD_HTML_CLOSE}'
    
    result = re.sub(pattern, lambda match: f'{CHORD_HTML_OPEN}{transport_chord(match.group(1), tune)}{CHORD_HTML_CLOSE}', text)
    
    return result


def md_to_Song(song: str, newtune: int) -> Song:
    file_md_path = MD_PATH + song + ".md"
    with open(file_md_path, 'r') as f:
        md_text = f.read()

    [md_header, md_song] = md_text.split(SEPARATOR)
    md_song = md_song.lstrip()
    md_header = "<pre>\n" + md_header + "\n</pre>"

    filename = song
    name = get_info_header(md_header, "Name")
    artist = get_info_header(md_header, "Artist")
    tune = int(get_info_header(md_header, "Tune")) + newtune
    song_html = transport_song(md_to_html(md_song), newtune)

    return Song(filename = filename, name = name, artist = artist, tune = tune, header = md_header, song_html = song_html)


def sum_tunes(t1: int, t2: int) -> int:
    return t1+t2


##########################################
#Handle of the chords positions
##########################################

class ChordPosition:
    def __init__(self, filename: str, name: str, text : str):
        self.filename = filename
        self.name = name
        self.text = text


def get_positions_list():
    positions_list_filename = [f for f in os.listdir(POSITIONS_PATH) if os.path.isfile(os.path.join(POSITIONS_PATH,f))]
    positions_list = [] 
    for i, filename in enumerate(positions_list_filename):
        newchordposition = ChordPosition(filename = filename, name = filename.removesuffix(".txt"), text = open(POSITIONS_PATH + filename, 'r').read())
        positions_list.append(newchordposition)
    return positions_list

