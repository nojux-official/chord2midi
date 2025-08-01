import argparse
import mido
from mido import MidiFile, MidiTrack, Message
from itertools import permutations, product
import random

def get_scale_root(root_input, octave=4):
    """
    Converts the scale root input to a MIDI note number.

    Parameters:
    - root_input (str): The input representing the scale root (e.g., 'C', 'Cmaj', 'D#', 'D#maj').
    - octave (int): The octave number. Default is 4.

    Returns:
    - int: The MIDI note number corresponding to the scale root.
    """

    # Define mappings of letters to semitones
    letter_to_semitone = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
    modifiers = {'#': 1, 'b': -1}

    # Parse the root input
    letter = root_input[0].upper()
    modifier = ''
    if len(root_input) > 1:
        modifier = root_input[1]
    
    # Calculate the semitone offset
    semitone_offset = letter_to_semitone[letter]
    if modifier in modifiers:
        semitone_offset += modifiers[modifier]

    # Convert to MIDI note number
    scale_root = 12 * (octave + 1) + semitone_offset  # Start from C4
    return scale_root

def get_chord_notes(scale_root: int, degree: int, chord_type='major', inversion=0):
    """
    Returns the notes for a specified chord degree in a major scale, with optional inversion.

    Parameters:
    - scale_root (int): The root note of the scale (as a MIDI note number).
    - degree (int): The degree of the chord in the scale (1 for tonic, 2 for supertonic, etc.).
    - chord_type (str): The type of chord ('major', 'minor', or 'diminished'). Defaults to 'major'.
    - inversion (int): The inversion of the chord (0=root, 1=first, 2=second). Defaults to 0.

    Returns:
    - list: A list of MIDI note numbers for the specified chord.
    """

    # Define the major scale intervals
    major_scale_intervals = [2, 2, 1, 2, 2, 2, 1]
    
    # Generate the major scale notes starting from the root
    scale_notes = [scale_root]
    current_note = scale_root
    for interval in major_scale_intervals[:-1]:  # Exclude last interval as we only need 7 notes
        current_note += interval
        scale_notes.append(current_note)
    
    # Adjust degree to zero-based index
    degree_index = degree - 1
    
    # Get the root note for this chord
    chord_root = scale_notes[degree_index]

    if chord_type == 'major':
        chord_intervals = [0, 4, 7]
    elif chord_type == 'minor':
        chord_intervals = [0, 3, 7]
    elif chord_type == 'diminished':
        chord_intervals = [0, 3, 6]
    else:
        raise ValueError("Unsupported chord type. Use 'major', 'minor', or 'diminished'.")

    # Calculate the chord notes based on the chord root
    chord_notes_midi = [chord_root + interval for interval in chord_intervals]

    # Apply inversion: move the lowest note(s) up an octave
    for i in range(inversion):
        chord_notes_midi[i] += 12

    # Sort to keep ascending order
    chord_notes_midi = sorted(chord_notes_midi)

    # Add the bass note an octave lower
    bass_note = chord_notes_midi[0] - 12
    chord_notes_midi.insert(0, bass_note)

    return chord_notes_midi

def create_midi(scale_root: int, chord_degrees, chord_types, output_file, chord_duration, inversions=None):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    # Always expect inversions as a list/tuple, default to all root position if None
    if inversions is None:
        inversions = [0] * len(chord_degrees)

    for degree, chord_type, inversion in zip(chord_degrees, chord_types, inversions):
        chord_notes = get_chord_notes(scale_root, degree, chord_type, inversion)
        for note in chord_notes:
            track.append(Message('note_on', note=note, velocity=64, time=0))
        track.append(Message('note_off', note=chord_notes[0], velocity=64, time=chord_duration))
        for note in chord_notes[1:]:
            track.append(Message('note_off', note=note, velocity=64, time=0))

    mid.save(output_file)
    print(f'MIDI file saved as {output_file}')

def create_midi_batch(scale_root, chord_degrees, chord_types, chord_duration):
    items = list(zip(chord_degrees, chord_types))
    scale_root_int = get_scale_root(scale_root)
    num_chords = len(chord_degrees)
    inversion_options = [0, 1, 2]

    for permutation in permutations(items):
        chordsOrd, typesOrd = zip(*permutation)
        # 1. Root position
        inversions_root = [0] * num_chords
        filename_root = auto_generate_filename(scale_root, chordsOrd, inversions_root)
        create_midi(scale_root_int, chordsOrd, typesOrd, filename_root, chord_duration, inversions_root)
        # 2. Random inversion for each chord
        inversions_random = [random.choice(inversion_options) for _ in range(num_chords)]
        filename_random = auto_generate_filename(scale_root, chordsOrd, inversions_random)
        create_midi(scale_root_int, chordsOrd, typesOrd, filename_random, chord_duration, inversions_random)

def auto_generate_filename(scale_root, chord_degrees, inversions=None):
    chord_degrees_str = ''.join(str(deg) for deg in chord_degrees)
    if inversions is not None and any(inv != 0 for inv in inversions):
        inversions_str = ''.join(str(inv) for inv in inversions)
        return f"{scale_root.upper()}_{chord_degrees_str}_{inversions_str}.midi"
    else:
        return f"{scale_root.upper()}_{chord_degrees_str}.midi"

def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate a MIDI file with a chord progression.')
    parser.add_argument('--scale-root', type=str, required=True, help='Root note of the scale (e.g., C, Cmaj)')
    parser.add_argument('--chord-degrees', type=int, nargs='+', required=True, help='Chord degrees in the scale (e.g., 6 4 1 5)')
    parser.add_argument('--chord-types', type=str, nargs='*', help='Chord types corresponding to the degrees (e.g., minor major major major)')
    parser.add_argument('--output-file', type=str, default=None, help='Output MIDI file name. If skipped, filename will be generated automatically.')
    parser.add_argument('--chord-duration', type=int, default=960, help='Duration of each chord in ticks. Default is 960 ticks.')
    parser.add_argument('--batch', action='store_true', help='Generate MIDI files for all permutations of chord degrees and types.')
    
    args = parser.parse_args()

    return args

if __name__ == '__main__':
    args = parse_arguments()

    if args.chord_types:
        if len(args.chord_degrees) != len(args.chord_types):
            raise ValueError("Number of chord types should match the number of chord degrees.")
        chord_types = args.chord_types
    else:
        # Automatically set chord types if not provided
        chord_types = []
        for degree in args.chord_degrees:
            if degree == 1 or degree == 4 or degree == 5:
                chord_types.append('major')
            elif degree == 2 or degree == 3 or degree == 6:
                chord_types.append('minor')
            elif degree == 7:
                chord_types.append('diminished')
            else:
                raise ValueError("Unsupported chord degree.")

    if args.batch:
        if args.output_file:
            raise ValueError("Batch mode does not support a single output file.")
        create_midi_batch(args.scale_root, args.chord_degrees, chord_types, args.chord_duration)
    else:
        # Generate filename if not provided
        if args.output_file is None:
            args.output_file = auto_generate_filename(args.scale_root, args.chord_degrees)
        
        scale_root = get_scale_root(args.scale_root)
        create_midi(scale_root, args.chord_degrees, chord_types, args.output_file, args.chord_duration)
