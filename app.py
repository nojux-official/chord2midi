from flask import Flask, request, jsonify, send_file
import os
from generate_midi import get_scale_root, create_midi, auto_generate_filename

app = Flask(__name__)

@app.route('/generate_midi', methods=['GET'])
def generate_midi():
    scale_root = request.args.get('scale_root', 'C')
    chord_degrees = request.args.getlist('chord_degrees', type=int)
    chord_types = request.args.getlist('chord_types')
    chord_duration = request.args.get('chord_duration', default=960, type=int)
    output_file = request.args.get('output_file')
    
    if not chord_degrees:
        return jsonify({'error': 'chord_degrees parameter is required'}), 400
    
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
    
    if output_file is None:
        output_file = auto_generate_filename(scale_root, chord_degrees)
    
    scale_root_midi = get_scale_root(scale_root)
    
    create_midi(scale_root_midi, chord_degrees, chord_types, output_file, chord_duration)
    
    return send_file(output_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
