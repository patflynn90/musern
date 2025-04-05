# src/renamer.py

import os
import logging
from typing import Dict, Optional

# Configure logging
logger = logging.getLogger(__name__)


def sanitize_string(input_str: str) -> str:
    """
    Replace all spaces with underscores and remove special characters.
    We'll allow letters, digits, and underscores. Everything else is stripped out.
    
    Args:
        input_str: The string to sanitize
        
    Returns:
        A sanitized string with spaces replaced by underscores and special characters removed
    """
    if not input_str:
        return ""

    # Replace spaces with underscores and filter out non-alphanumeric characters
    # More efficient approach using string methods
    return ''.join(c for c in input_str.replace(" ", "_") if c.isalnum() or c == "_")


def generate_new_filename(metadata: Dict[str, Optional[str]], original_path: str) -> str:
    """
    Generate a new filename following the pattern:
    {ARTIST} {ALBUM} {TRACK_NUMBER} {TRACK_NAME}.{EXTENSION}
    
    Where each segment is sanitized, and TRACK_NUMBER is zero-padded to 2 digits.
    If any metadata field is missing, it will be replaced with "Unknown".
    
    Args:
        metadata: Dictionary containing music metadata with keys:
                 - Artist: The primary artist
                 - Album: The album name
                 - Track No.: The track number
                 - Title: The track title
        original_path: Original file path to extract extension
        
    Returns:
        A new filename formatted according to the specified pattern
    """
    if not metadata:
        logger.warning("Empty metadata dictionary provided, using default values")
        metadata = {}
        
    if not original_path:
        logger.error("Empty original path provided")
        return "Unknown_Unknown_00_Unknown"

    artist = metadata.get("Artist") or "Unknown"
    album = metadata.get("Album") or "Unknown"
    track_no = metadata.get("Track No.") or "0"
    title = metadata.get("Title") or "Unknown"

    try:
        track_no_int = int(track_no)
        track_no_str = f"{track_no_int:02d}"
    except ValueError:
        logger.warning(f"Invalid track number '{track_no}', using '00'")
        track_no_str = "00"

    artist_clean = sanitize_string(artist)
    album_clean = sanitize_string(album)
    title_clean = sanitize_string(title)

    extension = os.path.splitext(original_path)[1]

    filename = f"{artist_clean} {album_clean} {track_no_str} {title_clean}{extension}"

    return filename


def rename_file(original_path: str, new_filename: str, dry_run: bool = False) -> Optional[str]:
    """
    Rename file at original_path to new_filename (no path included).
    If dry_run is True, only log the action without performing the rename.
    
    Args:
        original_path: Path to the original file
        new_filename: New filename to use (without path)
        dry_run: If True, only log what would happen without actually renaming
        
    Returns:
        The new path if successful, None if the operation failed or was skipped
    """
    if not original_path:
        logger.error("Empty original path provided")
        return None
        
    if not new_filename:
        logger.error("Empty new filename provided")
        return None
        
    if not os.path.exists(original_path):
        logger.error(f"Original file does not exist: {original_path}")
        return None

    dir_name = os.path.dirname(original_path)
    new_path = os.path.join(dir_name, new_filename)

    if os.path.exists(new_path):
        logger.warning(f"Target filename '{new_path}' already exists. Skipping.")
        return None

    if dry_run:
        logger.info(f"Dry-run: would rename '{original_path}' to '{new_path}'")
        return new_path

    try:
        os.rename(original_path, new_path)
        logger.info(f"Renamed '{original_path}' to '{new_path}'")
        return new_path
    except OSError as e:
        logger.error(f"Error renaming file '{original_path}' -> '{new_path}': {e}")
        return None
