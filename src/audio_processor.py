# src/audio_processor.py

from tinytag import TinyTag

def get_audio_metadata(file_path):
    """Extract and return metadata from an audio file."""
    try:
        audio = TinyTag.get(file_path)
        return {
            "Title": audio.title,
            "Artist": audio.artist,
            "Album Artist": audio.albumartist,
            "Track No.": audio.track,
            "Album": audio.album,
        }
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None
