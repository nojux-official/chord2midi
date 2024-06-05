from flask import Flask, request, jsonify, send_file, render_template_string, url_for
import os
from generate_midi import get_scale_root, create_midi, auto_generate_filename

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <title>Chord Progression MIDI Generator</title>
            <script src="https://cdn.jsdelivr.net/combine/npm/tone@14.7.58,npm/@magenta/music@1.23.1/es6/core.js,npm/focus-visible@5,npm/html-midi-player@1.5.0"></script>
          </head>
          <body>
            <div class="container">
              <h1>Chord Progression MIDI Generator</h1>
              <form id="midiForm" action="/generate_midi" method="get">
                <div>
                  <label for="scale_root">Scale Root:</label>
                  <input type="text" id="scale_root" name="scale_root" value="C">
                </div>
                <div>
                  <label for="chord_degrees">Chord Degrees:</label>
                  <input type="text" id="chord_degrees" name="chord_degrees" placeholder="e.g., 1,4,5">
                </div>
                <div>
                  <label for="chord_types">Chord Types (optional):</label>
                  <input type="text" id="chord_types" name="chord_types" placeholder="e.g., major,major,major">
                </div>
                <div>
                  <label for="chord_duration">Chord Duration:</label>
                  <input type="number" id="chord_duration" name="chord_duration" value="960">
                </div>
                <div>
                  <label for="output_file">Output File Name (optional):</label>
                  <input type="text" id="output_file" name="output_file" placeholder="e.g., my_chords.midi">
                </div>
                <button type="submit">Generate MIDI</button>
              </form>
              <div id="midiPreview" style="display:none;">
                <h2>MIDI Preview</h2>
                <midi-player id="midiPlayer" sound-font visualizer="#myVisualizer"></midi-player>
                <midi-visualizer type="piano-roll" id="myVisualizer"></midi-visualizer>
                <button id="downloadButton">Download MIDI</button>
              </div>
            </div>
            <script>
              document.getElementById('midiForm').onsubmit = function(event) {
                event.preventDefault();
                const form = event.target;
                const formData = new FormData(form);
                const queryString = new URLSearchParams(formData).toString();
                fetch('/generate_midi?' + queryString)
                  .then(response => response.json())
                  .then(data => {
                    if (data.error) {
                      alert(data.error);
                    } else {
                      document.getElementById('midiPreview').style.display = 'block';
                      const midiUrl = data.midi_url;
                      document.getElementById('midiPlayer').src = midiUrl;
                      document.getElementById('downloadButton').onclick = function() {
                        window.location.href = midiUrl;
                      };
                    }
                  })
                  .catch(error => console.error('Error:', error));
              };
            </script>
          </body>
        </html>
    ''')

@app.route('/generate_midi', methods=['GET'])
def generate_midi():
    scale_root = request.args.get('scale_root', 'C').strip()
    chord_degrees = request.args.get('chord_degrees', '').strip()
    chord_types = request.args.get('chord_types', '').strip()
    chord_duration = request.args.get('chord_duration', default=960, type=int)
    output_file = request.args.get('output_file', '').strip()
    
    if not chord_degrees:
        return jsonify({'error': 'chord_degrees parameter is required'}), 400
    
    chord_degrees = [int(deg.strip()) for deg in chord_degrees.split(',')]
    
    if not chord_types:
        chord_types = []
        for degree in chord_degrees:
            if degree == 1 or degree == 4 or degree == 5:
                chord_types.append('major')
            elif degree == 2 or degree == 3 or degree == 6:
                chord_types.append('minor')
            elif degree == 7:
                chord_types.append('diminished')
            else:
                return jsonify({'error': 'Unsupported chord degree'}), 400
    else:
        chord_types = [ctype.strip() for ctype in chord_types.split(',')]
    
    if not output_file:
        output_file = auto_generate_filename(scale_root, chord_degrees)
    
    scale_root_midi = get_scale_root(scale_root)
    
    create_midi(scale_root_midi, chord_degrees, chord_types, output_file, chord_duration)
    
    midi_url = url_for('get_midi_file', filename=output_file)
    return jsonify({'midi_url': midi_url})

@app.route('/midi_files/<filename>')
def get_midi_file(filename):
    return send_file(filename, as_attachment=False)

if __name__ == '__main__':
    app.run(debug=True)
