# musern

**musern** is a Python command-line utility designed to automatically rename music files based on their metadata. The goal of this project is to help users organize their music collections with consistent and meaningful file names.

## Current Status

**musern** is now fully functional and can both **read metadata** from music files and **rename files** based on their metadata.

## Features

### Current Features

- Extracts and displays metadata such as:
  - Title
  - Artist
  - Album
  - Track number
  - Album Artist
- Works with common audio file formats (e.g., MP3, FLAC)
- Automatically renames files using a consistent format: `{ARTIST} {ALBUM} {TRACK_NUMBER} {TRACK_NAME}.{EXTENSION}`
- Dry-run mode to preview changes without actually renaming files

### Planned Features

- Batch processing for large libraries
- Additional metadata editing and validation
- Customizable naming conventions

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/musern.git
cd musern

# Install dependencies
pip install -r requirements.txt
```

## Usage

**musern** provides two main commands:

### Display Metadata

To view the metadata of an audio file:

```bash
python -m src.main info /path/to/your/music/file.mp3
```

This will display all available metadata for the specified file.

### Rename Files

To rename an audio file based on its metadata:

```bash
python -m src.main rename /path/to/your/music/file.mp3
```

This will rename the file according to the format: `{ARTIST} {ALBUM} {TRACK_NUMBER} {TRACK_NAME}.{EXTENSION}`

#### Dry Run Mode

To preview renaming without actually changing the file:

```bash
python -m src.main rename --dry-run /path/to/your/music/file.mp3
```

## License

This project is licensed under the MIT License.
