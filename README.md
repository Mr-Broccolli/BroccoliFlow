![Python](https://img.shields.io/badge/Python-3.14.6-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Version](https://img.shields.io/badge/version-v1.8.0-orange)

# 🥦 BroccoliFlow

A professional-grade, high-performance file management utility that scans directories, organizes files into categorical folders, and provides atomic rollback capabilities.


## Features

### Advanced Organization & Performance

* **Concurrent Execution**: Utilizes `ThreadPoolExecutor` for high-speed file processing.

* **Intelligent Categorization**: Sorts files into Images, Documents, Videos, Audio, Archives, Installation Media, and Misc categories based on customizable rules.

* **Duplicate Protection**: Automatically detects filename collisions and resolves them with sequential renaming.

### Safety & Recovery

* **Undo System**: Records every file move in a persistent JSON operation log, allowing for full restoration to original locations.

* **Atomic Rollback**: Automatically triggers an emergency restoration if an organization process is interrupted or fails.

* **Dry-Run Mode**: Allows users to preview all proposed file movements without making any changes to the disk.

### Command-Line Interface

* **CLI Controller**: Fully refactored for terminal-based automation using `argparse`.

* **Direct Flags**: Supports streamlined workflows via `--source`, `--organize`, `--undo`, and `--dry-run`.

* **Robust Exits**: Implements safe `KeyboardInterrupt` handling for stable terminal sessions.

### Developer Experience & Tooling

* **Type Safety**: Full type hinting across the codebase for improved IDE support and static analysis.
* **Configuration Validation**: Automatic validation of `categories.json` with fallback to defaults and informative error messages.
* **Progress Reporting**: Real‑time console progress indicator (`Progress: X/Y files (Z%)`) during organization.
* **Professional Logging**: Rotating file logs (5 MB per file, 5 backups) with enriched format and optional console debug output.
* **CLI Enhancements**: `--max-workers` for adjustable parallelism, `--version` flag, improved help strings, and clean Ctrl+C handling.


## Current Status

Version: v1.8.0

* Folder validation & scanning
* Multi-threaded file organization
* Category-based sorting with custom configuration
* Operation logging & atomic rollback
* "Undo" restoration system
* CLI automation with dry-run support
* Performance-optimized (handles thousands of files efficiently)

### New Features in v1.8.0
* Type hints across all modules
* Configuration validation with fallback
* Real‑time progress reporting
* Professional logging with rotation and debug console
* Enhanced CLI (`--max-workers`, `--version`, better help, Ctrl+C handling)


## Screenshots

<p align="center">
  <img src="assets/screenshots/v1.7-main-menu.png" width="50%">
  <img src="assets/screenshots/v1.7-organization-report.png" width="34%">
</p>

<p align="center">
  <img src="assets/screenshots/v1.7-category-create.png" width="43%">
  <img src="assets/screenshots/v1.7-category-manager.png" width="24%">
</p>

<p align="center">
  <img src="assets/screenshots/v1.7-undo-summary.png" width="80%">
</p>



## Roadmap

### v1.0.0 - v1.7.0 ✅

* Concurrency, undo system, CLI architecture and dry-run functionality implemented.

### v1.8.0 ✅

* Type hints, CLI enhancements (`--max-workers`, `--version`, better help, Ctrl+C handling), configuration validation, progress reporting, professional logging system.

### v1.9.0

* Extended configuration schema validation and migration tools.

### v2.0.0

* Graphical User Interface (GUI) development.


## Installation

```bash
git clone https://github.com/Mr-Broccoli/BroccoliFlow.git
cd BroccoliFlow
python main.py --source "path/to/directory" --organize
```

## 📚 Project Files

* [CHANGELOG](./CHANGELOG.md)
* [LICENSE](./LICENSE)

## Tech Stack

* Python
* pathlib
* shutil
* ThreadPoolExecutor
* argparse

## Author

Nemo (Mr-Broccoli)