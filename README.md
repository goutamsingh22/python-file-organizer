# File Organizer

A Python script to organize files in a directory by their file extension. 
Uses `pathlib`, supports dry-run mode by default, and includes error handling.

## Requirements
- Python 3.6+

## Usage

### Preview (Dry Run) - Default
```bash
python file_organizer.py /path/to/directory
```
Or organize current directory:
```bash
python file_organizer.py .
```

### Actually Move Files
```bash
python file_organizer.py /path/to/directory --live
```

## Features
- Organizes files by extension into separate folders
- Dry-run mode by default (safe preview)
- Handles duplicate filenames automatically
- Error handling for permissions, missing directories
- Detailed summary report

## Example
```
[DRY RUN] Would move: photo.jpg -> jpg/photo.jpg
[DRY RUN] Would move: document.pdf -> pdf/document.pdf

Summary by extension:
  .jpg: 1 file(s)
  .pdf: 1 file(s)

==================================================
FILE ORGANIZATION REPORT
==================================================
Source: C:\Users\YourName\Downloads
Mode: DRY RUN (no changes made)
Files processed: 2
Errors: 0
==================================================
```
