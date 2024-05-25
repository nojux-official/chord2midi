import mido
from mido import MidiFile, MidiTrack, Message

# Create a new MIDI file
mid = MidiFile()

# Add a track to the MIDI file
track = MidiTrack()
mid.tracks.append(track)

# Define a list of notes to add to the MIDI file
notes = [60, 62, 64, 65, 67, 69, 71, 72]  # C major scale

# Add notes to the track
for note in notes:
    track.append(Message('note_on', note=note, velocity=64, time=0))
    track.append(Message('note_off', note=note, velocity=64, time=480))

# Save the MIDI file
output_file = 'output.mid'
mid.save(output_file)

print(f'MIDI file saved as {output_file}')
