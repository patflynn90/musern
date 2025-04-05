# src/audio_processor.py

from tinytag import TinyTag
from typing import Dict, Optional
import os
import logging

# Configure logging
logger = logging.getLogger(__name__)


def get_audio_metadata(file_path: str) -> Optional[Dict[str, Optional[str]]]:
    """
    Extract and return metadata from an audio file.
    
    This function uses TinyTag to extract common audio metadata fields including
    title, artist, album artist, track number, and album name.
    
    Args:
        file_path: Path to the audio file to extract metadata from
        
    Returns:
        A dictionary containing audio metadata with the following keys:
        - Title: The title of the track
        - Artist: The primary artist
        - Album Artist: The album artist (if different from primary artist)
        - Track No.: The track number on the album
        - Album: The album name
        
        Returns None if metadata extraction failed or if the file doesn't exist.
    """
    # Validate input
    if not file_path:
        logger.error("Empty file path provided")
        return None
        
    if not os.path.exists(file_path):
        logger.error(f"File does not exist: {file_path}")
        return None
        
    try:
        audio = TinyTag.get(file_path)
        return {
            "Title": audio.title,
            "Artist": audio.artist,
            "Album Artist": audio.albumartist,
            "Track No.": audio.track,
            "Album": audio.album,
        }
    except (IOError, OSError) as e:
        logger.error(f"File I/O error reading {file_path}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error reading file {file_path}: {e}")
        return None
