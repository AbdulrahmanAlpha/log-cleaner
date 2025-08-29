#!/usr/bin/env python3
"""
Log Cleaner Script
------------------

A DevOps-friendly Python tool that scans directories for old log files
and deletes them safely.

Features:
- CLI arguments with argparse
- Logging (INFO, DEBUG, ERROR)
- Dry-run mode (safe preview before deletion)
- Configurable age threshold in days
- Exit codes for CI/CD pipelines

Author: Abdulrahman A. Muhamad
GitHub: https://github.com/AbdulrahmanAlpha
"""

import sys
import argparse
import logging
from pathlib import Path
from datetime import datetime, timedelta

log = logging.getLogger("log-cleaner")

def setup_logging(verbose: bool) -> None:
    """Configure log format and verbosity."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    p = argparse.ArgumentParser(
        description="Clean up old log files from a directory."
    )
    p.add_argument("--path", type=Path, required=True, help="Target directory")
    p.add_argument("--days", type=int, default=30, help="Age threshold (days)")
    p.add_argument("--pattern", type=str, default="*.log", help="File pattern (default: *.log)")
    p.add_argument("--delete", action="store_true", help="Actually delete files (default: dry-run)")
    p.add_argument("-v", "--verbose", action="store_true", help="Verbose logging")
    return p.parse_args()

def files_older_than(path: Path, days: int, pattern: str) -> list[Path]:
    """Return list of files older than N days matching a pattern."""
    if not path.exists() or not path.is_dir():
        raise FileNotFoundError(f"Not a directory: {path}")
    cutoff = datetime.now() - timedelta(days=days)
    old_files: list[Path] = []
    for f in path.rglob(pattern):
        if f.is_file():
            try:
                mtime = datetime.fromtimestamp(f.stat().st_mtime)
                if mtime < cutoff:
                    old_files.append(f)
            except OSError as e:
                log.warning("Skipping %s (%s)", f, e)
    return old_files

def main() -> int:
    args = parse_args()
    setup_logging(args.verbose)
    log.debug("Args: %s", vars(args))

    try:
        candidates = files_older_than(args.path, args.days, args.pattern)
        if not candidates:
            log.info("No %s files older than %s days in %s",
                     args.pattern, args.days, args.path)
            return 0

        for f in candidates:
            if args.delete:
                try:
                    f.unlink()
                    log.info("Deleted: %s", f)
                except OSError as e:
                    log.error("Failed to delete %s (%s)", f, e)
                    return 1
            else:
                log.info("[DRY-RUN] Would delete: %s", f)

        if args.delete:
            log.info("Deletion completed.")
        else:
            log.info("Dry-run complete. Use --delete to apply.")
        return 0

    except FileNotFoundError as e:
        log.error(str(e))
        return 2
    except Exception as e:
        log.exception("Unhandled error: %s", e)
        return 3

if __name__ == "__main__":
    sys.exit(main())
