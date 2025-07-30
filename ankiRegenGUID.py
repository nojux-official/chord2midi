import sqlite3
import shutil
import os
import re

def extract_sound_filename(sound_field):
    """Extract sound filename from [sound:filename.wav] format"""
    match = re.search(r'\[sound:(.*?)\]', sound_field)
    return match.group(1) if match else None

def extract_guid_from_filename(sound_filename):
    """
    Extract GUID from sound filename (e.g., 'D_1456-hash.wav' -> 'D_1456')
    Ignores hash part after hyphen and .wav extension
    """
    if sound_filename:
        # Split on hyphen and take first part
        base_name = sound_filename.split('-')[0]
        # Remove .wav if present (shouldn't be needed but just in case)
        base_name = base_name.replace('.wav', '')
        return base_name
    return None

def regenerate_guids(apkg_file):
    """
    Read existing GUIDs and reapply them based on sound filename matching
    """
    temp_dir = 'temp_anki'
    os.makedirs(temp_dir, exist_ok=True)

    try:
        # Extract package
        shutil.unpack_archive(apkg_file, temp_dir, 'zip')

        # Connect to the database
        db = sqlite3.connect(os.path.join(temp_dir, 'collection.anki21'))
        cursor = db.cursor()

        # Update notes with new GUIDs
        updates = []
        cursor.execute("SELECT id, flds FROM notes")
        for note_id, fields in cursor.fetchall():
            fields = fields.split('\x1f')
            if fields:
                sound_filename = extract_sound_filename(fields[0])
                if sound_filename:
                    new_guid = extract_guid_from_filename(sound_filename)
                    if new_guid:
                        updates.append((new_guid, note_id))

        # Apply updates
        for new_guid, note_id in updates:
            cursor.execute("UPDATE notes SET guid = ? WHERE id = ?", 
                         (new_guid, note_id))
            print(f"Updated note {note_id} with GUID {new_guid}")
        
        db.commit()
        db.close()

        # Rebuild the package
        if os.path.exists(apkg_file):
            os.remove(apkg_file)
        shutil.make_archive(apkg_file[:-5], 'zip', temp_dir)
        os.rename(f"{apkg_file[:-5]}.zip", apkg_file)

        print(f"Successfully updated {len(updates)} notes with new GUIDs")

    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    APKG_FILE = "testing.apkg"  # Your deck file
    
    if not os.path.exists(APKG_FILE):
        print(f"Error: File {APKG_FILE} not found")
    else:
        regenerate_guids(APKG_FILE)