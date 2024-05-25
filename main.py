import argparse
import mido
from mido import MidiFile, MidiTrack, Message

def get_chord_notes(scale_root, degree, chord_type='major'):
    """
    Returns the notes for a specified chord degree in a major scale.

    Parameters:
    - scale_root (int): The root note of the scale (as a MIDI note number).
    - degree (int): The degree of the chord in the scale (1 for tonic, 2 for supertonic, etc.).
    - chord_type (str): The type of chord ('major' or 'minor'). Defaults to 'major'.

    Returns:
    - list: A list of MIDI note numbers for the specified chord.
    """

    # Define the major scale intervals
    major_scale_intervals = [2, 2, 1, 2, 2, 2, 1]
    
    # Generate the major scale notes starting from the root
    scale_notes = [scale_root]
    for interval in major_scale_intervals:
        scale_notes.append(scale_notes[-1] + interval)
    
    # Adjust degree to zero-based index
    degree_index = degree - 1

    if chord_type == 'major':
        # Major triad: root, major third, perfect fifth
        chord_intervals = [0, 4, 7]
    elif chord_type == 'minor':
        # Minor triad: root, minor third, perfect fifth
        chord_intervals = [0, 3, 7]
    else:
        raise ValueError("Unsupported chord type. Use 'major' or 'minor'.")

    # Calculate the chord notes
    chord_notes = [(scale_notes[degree_index] + interval) % 12 for interval in chord_intervals]

    # Convert chord notes to MIDI note numbers
    chord_notes_midi = [(scale_root + note) for note in chord_notes]

    return chord_notes_midi

def create_midi(scale_root, chord_degrees, chord_types, output_file, chord_duration):
    # Create a new MIDI file
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    # Add chords to the track
    for degree, chord_type in zip(chord_degrees, chord_types):
        chord_notes = get_chord_notes(scale_root, degree, chord_type)
        for note in chord_notes:
            track.append(Message('note_on', note=note, velocity=64, time=0))
        track.append(Message('note_off', note=chord_notes[0], velocity=64, time=chord_duration))
        for note in chord_notes[1:]:
            track.append(Message('note_off', note=note, velocity=64, time=0))

    # Save the MIDI file
    mid.save(output_file)
    print(f'MIDI file saved as {output_file}')

def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate a MIDI file with a chord progression.')
    parser.add_argument('--scale-root', type=int, required=True, help='Root note of the scale (MIDI note number)')
    parser.add_argument('--chord-degrees', type=int, nargs='+', required=True, help='Chord degrees in the scale (e.g., 6 4 1 5)')
    parser.add_argument('--chord-types', type=str, nargs='+', required=True, help='Chord types corresponding to the degrees (e.g., minor major major major)')
    parser.add_argument('--output-file', type=str, required=True, help='Output MIDI file name')
    parser.add_argument('--chord-duration', type=int, required=True, help='Duration of each chord in ticks')
    
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    create_midi(args.scale_root, args.chord_degrees, args.chord_types, args.output_file, args.chord_duration)
