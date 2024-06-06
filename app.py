from flask import Flask, request, jsonify, send_file, render_template, url_for
import os
from generate_midi import get_scale_root, create_midi, auto_generate_filename

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/games')
def games():
    return render_template('games.html')

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
