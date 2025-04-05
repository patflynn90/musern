# src/audio_processor.py

from tinytag import TinyTag
from typing import Dict, Optional, Union


def get_audio_metadata(file_path: str) -> Optional[Dict[str, Optional[str]]]:
    """
    Extract and return metadata from an audio file.
    
    Args:
        file_path: Path to the audio file to extract metadata from
        
    Returns:
        A dictionary containing audio metadata (Title, Artist, Album Artist, Track No., Album)
        or None if metadata extraction failed
    """
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
