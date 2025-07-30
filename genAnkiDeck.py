import genanki
import random
import os

# --- Configuration ---
DECK_NAME = 'Pop Progressions: Ear Training (I-V-vi-IV + Audio)'
OUTPUT_FILENAME = 'pop_progressions_Cmaj.apkg'
AUDIO_DIR = 'rec C'

def numbersToDegrees(numbers):
    '''
    Convert a list of integers to a string of chord degrees
    e.g., [1, 5, 6, 4] -> "I, V, vi, IV"
    '''
    degree_map = {
        1: 'I',
        2: 'ii',
        3: 'iii',
        4: 'IV',
        5: 'V',
        6: 'vi',
        7: 'vii°'
    }
    return ' - '.join(degree_map.get(num, str(num)) for num in numbers)

def analyzeFileName(filename):
    parts = filename[:-4].split('_')  # Remove '.wav' and split by '_'
    if len(parts) == 2:
        key = parts[0]
        key = f"{key} major"
        chord_degrees = parts[1]
        chord_degrees = [int(d) for d in chord_degrees] 
        chord_degrees = numbersToDegrees(chord_degrees)
        # meaning_text = f"{key} - {numbersToDegrees(chord_degrees)}"
        return filename, key, chord_degrees

def generateCardData():
    '''
    list directory of wav files in AUDIO_DIR
    the filename are in format of "{key}_{chord_degrees}.wav"
    key is a single letter (C, D, E, F, G, A, B)
    and chord_degrees is a list of integers (1, 2, 3, 4, 5, 6, 7)
    based on the chord degrees, generate a list of tuples
    where each tuple contains the filename and the text meaning
    file name example "C_1564.wav"
    '''
    card_data = []
    for sound_filename in os.listdir(AUDIO_DIR):
        if sound_filename.endswith('.wav'):
            # Extract key and chord degrees from the filename
            sound_filename, key, meaning_text = analyzeFileName(sound_filename)
            card_data.append((sound_filename, key, meaning_text))

    return card_data


def extract_guid_from_filename(sound_filename):
    """
    Extract GUID from sound filename (e.g., 'D_1456-hash.wav' -> 'D_1456')
    Ignores hash part after hyphen and .wav extension
    """
    if sound_filename:
        base_name = sound_filename.split('-')[0]
        base_name = base_name.replace('.wav', '')
        return base_name
    return None

# --- 1. Define a Model (Note Type) ---
my_model_id = 1607590219

sound_text_model = genanki.Model(
    my_model_id,
    'Sound & Text Model',
    fields=[
        {'name': 'Sound'},
        {'name': 'Scale'},
        {'name': 'Meaning'},
    ],
    templates=[
        {
            'name': 'Sound to Text Card',
            'qfmt': '{{Scale}}<br>{{Sound}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Meaning}}',
        },
    ],
    css='''
        .card {
            font-family: Arial;
            font-size: 24px;
            text-align: center;
            color: #333;
            background-color: #f5f5f5;
        }
        .meaning {
            font-weight: bold;
            color: #007bff; /* A nice blue for the meaning */
        }
    '''
)

# --- 2. Create a Deck ---
my_deck_id = 1539206123

my_deck = genanki.Deck(
    my_deck_id,
    DECK_NAME
)

# --- 3. Prepare Notes and Media Files ---
all_media_files = []
card_data = generateCardData()


for sound_filename, key, meaning_text in card_data:
    audio_file_path = os.path.join(AUDIO_DIR, sound_filename)

    if not os.path.exists(audio_file_path):
        print(f"Warning: Audio file not found: {audio_file_path}. Skipping this note.")
        continue

    all_media_files.append(audio_file_path)

    anki_sound_tag = f"[sound:{sound_filename}]"
    
    guid = extract_guid_from_filename(sound_filename)
    
    note = genanki.Note(
        model=sound_text_model,
        fields=[anki_sound_tag, key, meaning_text],
        guid=guid
    )
    my_deck.add_note(note)

# --- 4. Create a Package and Write to File ---
my_package = genanki.Package(my_deck)
my_package.media_files = all_media_files

try:
    my_package.write_to_file(OUTPUT_FILENAME)
    print(f"Anki deck '{OUTPUT_FILENAME}' generated successfully with {len(card_data)} notes and {len(all_media_files)} media files!")
except Exception as e:
    print(f"Error generating Anki deck: {e}")