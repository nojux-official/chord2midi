# chord2midi

This Python script generates a MIDI file with a chord progression based on the specified parameters.

## CLI usage

`python generate_midi.py --scale-root C --chord-degrees 1 4 5 --output-file cmaj_145.midi`

This command will generate a MIDI file named cmaj_145.midi with a chord progression of C major, F major, and G major chords.

### Arguments
* --scale-root: The root note of the scale (e.g., C, Cmaj). Default is C.
* --chord-degrees: Chord degrees in the scale (e.g., 6 4 1 5).
* --chord-types: Chord types corresponding to the degrees (e.g., minor major major major).
* --output-file: Output MIDI file name. If skipped, filename will be generated automatically.
* --chord-duration: Duration of each chord in ticks. Default is 960 ticks.

## API usage
Start a server using: `python app.py`
The server will be started on port 5000.

A sample request with curl to be saved on generated_midi.midi: 

```curl -G "http://127.0.0.1:5000/generate_midi" --data-urlencode "scale_root=C" --data-urlencode "chord_degrees=1" --data-urlencode "chord_degrees=4" --data-urlencode "chord_degrees=5" --data-urlencode "chord_duration=960" --output generated_midi.midi```

Or directly via a browser with the following url:
`http://127.0.0.1:5000/generate_midi?scale_root=C&chord_degrees=1&chord_degrees=4&chord_degrees=5&chord_duration=960`

### Query Parameters
* scale_root: The root note of the scale (e.g., C, Cmaj). Default is C.
* chord_degrees: Chord degrees in the scale (e.g., 6, 4, 1, 5). Specify each degree as a separate parameter.
* chord_types: (Optional) Chord types corresponding to the degrees (e.g., minor, major, major, major). Specify each type as a separate parameter.
* output_file: (Optional) Output MIDI file name. If skipped, the filename will be generated automatically.
* chord_duration: (Optional) Duration of each chord in ticks. Default is 960 ticks.

## Dependencies
* Python 3.x version
* mido and flask libraries (Install using `pip install -r requirements.txt`)

Tested with Python 3.10.7

## Acknowledgements
This project acknowledges ChatGPT's role in its creation. It aimed to check ChatGPT's coding capabilities for quick project creation.
