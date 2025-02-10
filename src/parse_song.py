import os
import yaml
import re

# Read the config
with open('config.yaml', 'r') as f:
    config_data = yaml.load(f, Loader=yaml.SafeLoader)

MD_PATH = config_data.get("MD_PATH")
CHORD_MD_OPEN = config_data.get("CHORD_MD_OPEN")
CHORD_MD_CLOSE = config_data.get("CHORD_MD_CLOSE")


def parse_song(file_name : str, chords : list[str]):
    file_path = MD_PATH + file_name
    with open(file_path, 'r') as f:
        text = f.read()
    
    # remove empty lines
    text = re.sub(r'\n\s*\n', '\n', text)

    # X -> <X>
    for c in chords:
        text = re.sub(rf'\n{c}\n', f'\n{CHORD_MD_OPEN}{c}{CHORD_MD_CLOSE}\n', text) 
        text = re.sub(rf'\n{c}  ', f'\n{CHORD_MD_OPEN}{c}{CHORD_MD_CLOSE}', text) 
        text = re.sub(rf' {c} ', f'{CHORD_MD_OPEN}{c}{CHORD_MD_CLOSE}', text) 
        text = re.sub(rf'{c}  ', f'{CHORD_MD_OPEN}{c}{CHORD_MD_CLOSE}', text) 
        text = re.sub(rf'  {c}', f'{CHORD_MD_OPEN}{c}{CHORD_MD_CLOSE}', text) 

    with open(file_path, "w") as f:
        f.write(text) 


def parse_from_list():
    files = sorted(os.listdir(MD_PATH))
    for i, file in enumerate(files):
        print(f"{i}. {file}")

    print("Enter the number of the file you want to parse:")
    file_name = files[int(input())]
    input_chords = input("Enter the chords separated by space: ")
    parse_song(file_name, input_chords.split(" "))

parse_from_list()


    
