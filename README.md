# chord2midi

This Python script generates a MIDI file with a chord progression based on the specified parameters.

## Usage

`python generate_midi.py --scale-root C --chord-degrees 1 4 5 --output-file cmaj_145.midi`

This command will generate a MIDI file named cmaj_145.midi with a chord progression of C major, F major, and G major chords.

### Arguments
* --scale-root: The root note of the scale (e.g., C, Cmaj). Default is C.
* --chord-degrees: Chord degrees in the scale (e.g., 6 4 1 5).
* --chord-types: Chord types corresponding to the degrees (e.g., minor major major major).
* --output-file: Output MIDI file name. If skipped, filename will be generated automatically.
* --chord-duration: Duration of each chord in ticks. Default is 960 ticks.

## Dependencies
Python 3.x
mido library (Install using `pip install mido`)

## Acknowledgements
This project acknowledges ChatGPT's role in its creation. It aimed to check ChatGPT's coding capabilities for quick project creation.
