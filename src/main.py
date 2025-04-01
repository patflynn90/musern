# src/main.py

import argparse
import os

from src.audio_processor import get_audio_metadata

# src/main.py


def main():
    """Main function to extract and display metadata from an audio file."""
    parser = argparse.ArgumentParser(description="Extract metadata from an audio file")
    parser.add_argument("file_path", type=str, help="Path to the audio file")

    args = parser.parse_args()
    metadata = get_audio_metadata(args.file_path)

    if metadata:
        for key, value in metadata.items():
            print(f"{key}: {value}")
    else:
        print("Failed to extract metadata.")


if __name__ == "__main__":
    main()
