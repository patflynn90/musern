# src/renamer.py

import os
import re


def sanitize_string(input_str):
    """
    Replace all spaces with underscores and remove special characters.
    We'll allow letter, digits, and underscores.
    Everything else is stripped out.
    """
    if not input_str:
        return ""

    temp = input_str.replace(" ", "_")

    temp = re.sub(r"[^A-Za-z0-9_]+", "", temp)

    return temp


def generate_new_filename(metadata, original_path):
    """
    Generate a new filename following:
    {ARTIST} {ALBUM} {TRACK_NUMBER} {TRACK_NAME}.{EXTENSION}
    Where each segment is sanitized, and TRACK_NUMBER is zero-padded to 2 digits.
    """

    artist = metadata.get("Artist") or "Unknown"
    album = metadata.get("Album") or "Unknown"
    track_no = metadata.get("Track No.") or "0"
    title = metadata.get("Title") or "Unknown"

    try:
        track_no_int = int(track_no)
        track_no_str = f"{track_no_int:02d}"
    except ValueError:
        track_no_str = "00"

    artist_clean = sanitize_string(artist)
    album_clean = sanitize_string(album)
    title_clean = sanitize_string(title)

    extension = os.path.splitext(original_path)[1]

    filename = f"{artist_clean} {album_clean} {track_no_str} {title_clean}{extension}"

    return filename


def rename_file(original_path, new_filename, dry_run=False):
    """
    Rename file at original_path to new_filename (no path included).
    If dry_run is True, only print out the action without performing the rename.
    """

    dir_name = os.path.dirname(original_path)
    new_path = os.path.join(dir_name, new_filename)

    if os.path.exists(new_path):
        print(f"Target filename '{new_path}' already exists. Skipping.")
        return None

    if dry_run:
        print(f"Dry-run: would rename '{original_path}' to '{new_path}'")
        return new_path

    try:
        os.rename(original_path, new_path)
        print(f"Renamed '{original_path}' to '{new_path}'")
        return new_path
    except OSError as e:
        print(f"Error renaming file '{original_path}' -> '{new_path}': {e}")
        return None
