import os
import subprocess
from pathlib import Path
from typing import List

def midi_to_wav(midi_file: str, soundfont_path: str = "default.sf2", output_path: str = None) -> str:
    """
    Convert a MIDI file to WAV using FluidSynth
    
    Args:
        midi_file (str): Path to the input MIDI file
        soundfont_path (str): Path to the soundfont file (default: default.sf2)
        output_path (str): Path for the output WAV file (optional)
    
    Returns:
        str: Path to the generated WAV file
    """
    if not os.path.exists(midi_file):
        raise FileNotFoundError(f"MIDI file not found: {midi_file}")
    
    if not os.path.exists(soundfont_path):
        raise FileNotFoundError(f"Soundfont file not found: {soundfont_path}")
    
    # If no output path specified, use the same path as MIDI but with .wav extension
    if output_path is None:
        output_path = str(Path(midi_file).with_suffix('.wav'))
    
    try:
        # Convert MIDI to WAV
        subprocess.run([
            'fluidsynth',
            '-gain', '5',
            '-ni',
            '-F', output_path,
            '-r', '44100',
            soundfont_path,
            midi_file,
        ], check=True)
        
        return output_path
        
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Conversion failed: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"An error occurred: {str(e)}")

def convert_directory(input_dir: str, soundfont_path: str = "default.sf2", output_dir: str = None) -> List[str]:
    """
    Convert all MIDI files in a directory to WAV
    
    Args:
        input_dir (str): Path to the input directory containing MIDI files
        soundfont_path (str): Path to the soundfont file
        output_dir (str): Path to the output directory (optional)
    
    Returns:
        List[str]: List of paths to the generated WAV files
    """
    input_path = Path(input_dir)
    if not input_path.is_dir():
        raise NotADirectoryError(f"Input directory not found: {input_dir}")
    
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
    
    converted_files = []
    midi_files = list(input_path.glob("*.midi")) + list(input_path.glob("*.mid"))
    
    for midi_file in midi_files:
        if output_dir:
            output_file = str(output_path / midi_file.with_suffix('.wav').name)
        else:
            output_file = None
        
        try:
            result = midi_to_wav(str(midi_file), soundfont_path, output_file)
            converted_files.append(result)
            print(f"Converted: {midi_file.name} → {Path(result).name}")
        except Exception as e:
            print(f"Failed to convert {midi_file.name}: {str(e)}")
    
    return converted_files

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Convert MIDI files to WAV")
    parser.add_argument("input_dir", help="Directory containing input MIDI files")
    parser.add_argument("--soundfont", default="default.sf2", help="Path to the soundfont file")
    parser.add_argument("--output-dir", help="Directory for output WAV files")
    
    args = parser.parse_args()
    
    try:
        converted = convert_directory(args.input_dir, args.soundfont, args.output_dir)
        print(f"\nSuccessfully converted {len(converted)} files")
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)