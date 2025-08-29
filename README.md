# 🧹 Log Cleaner Script: DevOps Python Tool

This project contains a Python script that automatically scans directories for old log files and safely deletes them.
It’s designed with **DevOps practices in mind**: automation, observability, safety, and CI/CD compatibility.

---

## 📜 What This Script Does

* ✅ **Finds log files** (`*.log` by default) older than a specified number of days.
* ✅ **Dry-run mode** to preview what would be deleted before actually doing it.
* ✅ **Verbose logging** with timestamps and log levels.
* ✅ **Configurable CLI arguments** with `argparse`.
* ✅ **Exit codes** to integrate cleanly with CI/CD pipelines.
* ✅ **Error handling** so pipelines won’t break unexpectedly.

---

## ⚙️ How It Works (Concept by Concept)

Let’s break down the script:

### 1. Shebang & Documentation

```python
#!/usr/bin/env python3
"""
Log Cleaner Script
"""
```

* **`#!/usr/bin/env python3`** → lets you run the script directly (`./log_cleaner.py`) without typing `python3`.
* **Docstring (`"""..."""`)** → documents purpose & features for future maintainers.

---

### 2. Imports

```python
import sys, argparse, logging
from pathlib import Path
from datetime import datetime, timedelta
```

* **sys** → handles exit codes for pipelines.
* **argparse** → adds CLI arguments (like `--path /var/log`).
* **logging** → structured logs with timestamps.
* **pathlib** → modern way to work with file paths.
* **datetime/timedelta** → calculate file ages.

---

### 3. Logging Setup

```python
def setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
```

* Configures how logs look.
* **Verbose mode** = show debug details.
* Log format example:

  ```
  2025-08-26 12:00:00 | INFO | Deleted: /var/log/error.log
  ```

---

### 4. Argument Parsing

```python
def parse_args():
    p = argparse.ArgumentParser(description="Clean up old log files")
    p.add_argument("--path", type=Path, required=True, help="Target directory")
    p.add_argument("--days", type=int, default=30, help="Age threshold")
    p.add_argument("--pattern", type=str, default="*.log", help="File pattern")
    p.add_argument("--delete", action="store_true", help="Actually delete files")
    p.add_argument("-v", "--verbose", action="store_true", help="Verbose logging")
    return p.parse_args()
```

* Adds CLI flags:

  * `--path /var/log` → directory to scan.
  * `--days 30` → threshold for old files.
  * `--pattern '*.log'` → filter by filename pattern.
  * `--delete` → required to actually delete.
  * `-v` → enable detailed logs.

✅ Example:

```bash
./log_cleaner.py --path /var/log --days 14 --delete -v
```

---

### 5. File Scanner

```python
def files_older_than(path: Path, days: int, pattern: str) -> list[Path]:
    cutoff = datetime.now() - timedelta(days=days)
    old_files = []
    for f in path.rglob(pattern):
        if f.is_file() and datetime.fromtimestamp(f.stat().st_mtime) < cutoff:
            old_files.append(f)
    return old_files
```

* Loops through directory recursively.
* Checks last modification time of each file.
* Collects files older than cutoff.

✅ DevOps Use: find old logs to archive or clean up.

---

### 6. Main Logic

```python
def main() -> int:
    args = parse_args()
    setup_logging(args.verbose)

    candidates = files_older_than(args.path, args.days, args.pattern)
    if not candidates:
        log.info("No files found")
        return 0

    for f in candidates:
        if args.delete:
            f.unlink()
            log.info("Deleted: %s", f)
        else:
            log.info("[DRY-RUN] Would delete: %s", f)
```

* If no files are found → log + exit.
* If files found → loop through them:

  * If `--delete` → delete the file.
  * Else → log what would be deleted.

✅ This prevents accidents (safe by default).

---

### 7. Exit Codes

```python
if __name__ == "__main__":
    sys.exit(main())
```

* Returns an exit code:

  * `0` → success
  * `1` → deletion failed
  * `2` → invalid directory
  * `3` → unexpected error

✅ CI/CD pipelines rely on these codes to fail/pass builds.

---

## 🚀 Usage Examples

### Dry-Run Mode (safe)

```bash
./log_cleaner.py --path /var/log --days 30
```

Output:

```
2025-08-26 12:10:00 | INFO | [DRY-RUN] Would delete: /var/log/app/error.log
```

### Verbose Mode

```bash
./log_cleaner.py --path /tmp --days 7 -v
```

### Actual Deletion

```bash
./log_cleaner.py --path /tmp --days 14 --delete
```

---

## 🛠 DevOps Scenarios

* **Server maintenance** → clean up `/var/log` to free space.
* **CI/CD pipelines** → run as a job to keep workspaces clean.
* **Containers** → avoid disk bloat inside Docker images.
* **Cloud environments** → automate log retention policies.

---

## 📂 Repo Setup

Clone the repo:

```bash
git clone https://github.com/AbdulrahmanAlpha/log-cleaner.git
cd log-cleaner
chmod +x log_cleaner.py
```

Run:

```bash
./log_cleaner.py --path /var/log --days 30
```

---

## 🔑 Key Takeaways

This script demonstrates:

* **Python scripting for automation**
* **Safe DevOps practices (dry-run, logging, exit codes)**
* **Portfolio-quality code** → shows you know how to design reusable tools.

## 📜 LICENSE (MIT)


```txt
MIT License
Copyright (c) 2025 Abdulrahman

Permission is hereby granted, free of charge, to any person obtaining a copy
```
### 👨‍💻 Author: Abdulrahman A. Muhamad