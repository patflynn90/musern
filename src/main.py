# src/main.py

import argparse
import os
import logging
import sys
from typing import Optional, Dict, Any

from src.audio_processor import get_audio_metadata
from src.renamer import generate_new_filename, rename_file

# Configure logging
logger = logging.getLogger(__name__)


def setup_logging(verbose: bool = False) -> None:
    """
    Configure logging for the application.
    
    Args:
        verbose: If True, set log level to DEBUG, otherwise INFO
    """
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def main() -> None:
    """
    Main entry point for the application.
    Sets up command-line argument parsing and dispatches to appropriate handlers.
    """
    parser = argparse.ArgumentParser(
        prog="musern", description="Manage audio metadata and rename audio files."
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
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
    
    # Setup logging based on verbosity
    setup_logging(args.verbose)
    
    logger.debug("Starting application with arguments: %s", args)

    if args.command == "info":
        handle_info_command(args.file_path)
    elif args.command == "rename":
        handle_rename_command(args.file_path, args.dry_run)
    else:
        parser.print_help()


def handle_info_command(file_path: str) -> None:
    """
    Handle the 'info' subcommand by displaying metadata for the specified audio file.
    
    Args:
        file_path: Path to the audio file to extract metadata from
    """
    if not file_path:
        logger.error("Empty file path provided")
        return
        
    if not os.path.exists(file_path):
        logger.error(f"File does not exist: {file_path}")
        return
        
    logger.info(f"Extracting metadata from: {file_path}")
    metadata = get_audio_metadata(file_path)
    
    if metadata:
        logger.info("Metadata extracted successfully")
        for key, value in metadata.items():
            print(f"{key}: {value}")
    else:
        logger.error("Failed to extract metadata from file: %s", file_path)
        print("Failed to extract metadata.")


def handle_rename_command(file_path: str, dry_run: bool) -> None:
    """
    Handle the 'rename' subcommand by renaming the specified audio file based on its metadata.
    
    Args:
        file_path: Path to the audio file to rename
        dry_run: If True, only preview the renaming without actually doing it
    """
    if not file_path:
        logger.error("Empty file path provided")
        return
        
    if not os.path.exists(file_path):
        logger.error(f"File does not exist: {file_path}")
        return
        
    logger.info(f"Processing file for renaming: {file_path}")
    metadata = get_audio_metadata(file_path)
    
    if not metadata:
        logger.error("Failed to extract metadata. Cannot rename file: %s", file_path)
        print("Failed to extract metadata. Cannot rename.")
        return

    new_filename = generate_new_filename(metadata, file_path)
    logger.info(f"Generated new filename: {new_filename}")
    
    result = rename_file(file_path, new_filename, dry_run=dry_run)
    if result:
        logger.info("File renamed successfully")
    else:
        logger.warning("File rename operation did not complete successfully")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Application terminated by user")
        sys.exit(0)
    except Exception as e:
        logger.exception("Unexpected error: %s", e)
        sys.exit(1)
