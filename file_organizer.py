#!/usr/bin/env python3
"""
File Organizer - Organizes files by extension
Supports dry-run mode and error handling
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class FileOrganizer:
    def __init__(self, source_dir: str, dry_run: bool = True):
        self.source_dir = Path(source_dir).resolve()
        self.dry_run = dry_run
        self.moved_files: List[Tuple[Path, Path]] = []
        self.errors: List[Tuple[Path, str]] = []
        
        if not self.source_dir.exists():
            raise FileNotFoundError(f"Source directory does not exist: {self.source_dir}")
        if not self.source_dir.is_dir():
            raise NotADirectoryError(f"Source path is not a directory: {self.source_dir}")
    
    def organize(self) -> Dict[str, int]:
        """
        Organize files by extension
        Returns dict with counts per extension
        """
        counts: Dict[str, int] = {}
        
        try:
            for item in self.source_dir.iterdir():
                if item.is_file():
                    try:
                        ext = item.suffix.lower().lstrip('.') or 'no_extension'
                        dest_dir = self.source_dir / ext
                        dest_path = dest_dir / item.name
                        
                        # Handle duplicate filenames
                        counter = 1
                        original_stem = item.stem
                        original_suffix = item.suffix
                        while dest_path.exists():
                            dest_path = dest_dir / f"{original_stem}_{counter}{original_suffix}"
                            counter += 1
                        
                        if self.dry_run:
                            print(f"[DRY RUN] Would move: {item.name} -> {ext}/{dest_path.name}")
                        else:
                            dest_dir.mkdir(parents=True, exist_ok=True)
                            item.rename(dest_path)
                            print(f"Moved: {item.name} -> {ext}/{dest_path.name}")
                        
                        self.moved_files.append((item, dest_path))
                        counts[ext] = counts.get(ext, 0) + 1
                        
                    except (PermissionError, OSError) as e:
                        error_msg = f"Failed to process {item.name}: {e}"
                        self.errors.append((item, error_msg))
                        print(f"ERROR: {error_msg}", file=sys.stderr)
                        
        except PermissionError as e:
            print(f"ERROR: Cannot access directory {self.source_dir}: {e}", file=sys.stderr)
            sys.exit(1)
        
        return counts
    
    def report(self):
        """Print summary report"""
        print("\n" + "="*50)
        print("FILE ORGANIZATION REPORT")
        print("="*50)
        print(f"Source: {self.source_dir}")
        print(f"Mode: {'DRY RUN (no changes made)' if self.dry_run else 'LIVE (files moved)'}")
        print(f"Files processed: {len(self.moved_files)}")
        print(f"Errors: {len(self.errors)}")
        print("="*50)


def main():
    parser = argparse.ArgumentParser(
        description="Organize files in a directory by their file extension",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run (preview changes) - default
  python file_organizer.py /path/to/directory
  
  # Actually move files
  python file_organizer.py /path/to/directory --live
  
  # Organize current directory
  python file_organizer.py .
        """
    )
    parser.add_argument('directory', nargs='?', default='.', 
                        help='Directory to organize (default: current directory)')
    parser.add_argument('--live', action='store_true',
                        help='Actually move files (default is dry-run mode)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview changes without moving files (default)')
    
    args = parser.parse_args()
    
    # Default to dry-run unless --live is specified
    dry_run = not args.live
    
    try:
        organizer = FileOrganizer(args.directory, dry_run=dry_run)
        counts = organizer.organize()
        
        if counts:
            print("\nSummary by extension:")
            for ext, count in sorted(counts.items()):
                print(f"  .{ext}: {count} file(s)")
        else:
            print("\nNo files to organize.")
        
        organizer.report()
        
    except (FileNotFoundError, NotADirectoryError, PermissionError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
