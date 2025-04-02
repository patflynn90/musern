# src/main.py

import argparse
import os

from src.audio_processor import get_audio_metadata
from src.renamer import generate_new_filename, rename_file


def main():
    parser = argparse.ArgumentParser(
        prog="musern", description="Manage audio metadata and rename audio files."
    )
    subparsers = parser.add_subparsers(dest="command", help="Sub-command to run")

    # info sub-command
    parser_info = subparsers.add_parser(
        "info", help="Extract and display metadata from an audio file"
    )
    parser_info.add_argument("file_path", type=str, help="Path to the audio file")

    # rename sub-command
    parser_rename = subparsers.add_parser(
        "rename", help="Rename the audio file based on metadata"
    )
    parser_rename.add_argument("file_path", type=str, help="Path to the audio file")
    parser_rename.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview renaming without actually doing it",
    )

    args = parser.parse_args()

    if args.command == "info":
        handle_info_command(args.file_path)
    elif args.command == "rename":
        handle_rename_command(args.file_path, args.dry_run)
    else:
        parser.print_help()


def handle_info_command(file_path):
    metadata = get_audio_metadata(file_path)
    if metadata:
        for key, value in metadata.items():
            print(f"{key}: {value}")
    else:
        print("Failed to extract metadata.")


def handle_rename_command(file_path, dry_run):
    metadata = get_audio_metadata(file_path)
    if not metadata:
        print("Failed to extract metadata. Cannot rename.")
        return

    new_filename = generate_new_filename(metadata, file_path)
    rename_file(file_path, new_filename, dry_run=dry_run)


if __name__ == "__main__":
    main()
