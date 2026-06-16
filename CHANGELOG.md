# Changelog

All notable changes to this project are documented in this file.

---

## [1.7.0] - 2026-06-16

### Added

* **Command-Line Interface (CLI)**: Implemented `argparse` to support terminal-based execution.
* **Direct Execution Flags**: Introduced support for `--source`, `--organize`, and `--undo` to enable automation.
* **Interrupt Handling**: Added robust `KeyboardInterrupt` management to ensure clean exits during terminal sessions.

### Improved

* **Architecture**: Decoupled the interactive UI from core logic, allowing for dual-mode execution (Menu vs. CLI).
* **Automation**: Standardized flag behavior to integrate seamlessly with system task schedulers.
* **Responsiveness**: Enhanced signal handling for better performance in non-interactive terminal environments.

> **TL;DR**: BroccoliFlow is now a professional CLI utility. You can bypass the menus and automate your file organization directly from your terminal.

---

## [1.6.0] - 2026-06-14

### Added

* **Concurrent File Operations**: Integrated `ThreadPoolExecutor` for high-performance, multi-threaded file movement.
* **Atomic Rollback Mechanism**: Implemented safety checks to restore state if transfers fail.
* **Performance Tracking**: Added real-time transfer speed measurements.
* **Undo System**: Created a persistent JSON-based log system to track and reverse file moves.
* **Configuration Management**: Moved state to a dedicated `config/` directory with filesystem flushing (`fsync`).

### Improved

* **Structural Refactor**: Modularized logic into dedicated files (`organizer.py`, `undo.py`, `categories.py`).
* **Data Integrity**: Forced OS buffer writes to prevent corruption during configuration changes.
* **Resource Management**: Excluded logs from scan targets to prevent infinite recursive loops.

> **TL;DR**: Major speed and safety upgrade. Concurrent moves make it fast; atomic rollbacks and undo history make it bulletproof.

---

## [1.5.0] - 2026-06-10

### Added

* **Undo Functionality**: Implemented the first iteration of the "Undo Last Organization" feature.
* **Logging**: Automated creation of operation history logs.
* **Startup Interface**: Introduced a menu-based system for easier navigation.

### Improved

* **Workflow Safety**: Added validation for all user menu inputs.
* **Recovery**: Enhanced file management to support post-organization restoration.

> **TL;DR**: Added the "undo" button. You can now recover from mistakes with a structured log-based restoration system.

---

## [1.4.0] - 2026-06-05

### Added

* **Duplicate Protection**: Logic to detect and prevent overwriting existing files.
* **Smart Renaming**: Automated sequential numbering for duplicate file collision resolution.

### Improved

* **Safety**: Shifted from simple moves to collision-free path management.

> **TL;DR**: Files no longer vanish! If you have two files named the same, BroccoliFlow now handles them safely.

---

## [1.3.0] - 2026-06-01

### Added

* **Category Sorting**: Implemented automatic folder-based categorization.
* **Detection**: Added specific recognition for archive formats and installers.
* **Reporting**: Added a summary report to show file counts after organization.

### Improved

* **UX**: Provided clearer path previews before moving files.

> **TL;DR**: The "organizer" is now real. It sorts files into folders by type and gives you a summary of the work done.

---

## [1.2.0] - 2026-05-25

### Added

* **File Analysis**: Enabled basic folder scanning and type detection.
* **Classification**: Added initial logical grouping for files.

### Improved

* **Metrics**: Enhanced scan statistics for better user visibility.

> **TL;DR**: The engine learned how to "read" your folder contents and group them logically.

---

## [1.1.0] - 2026-05-20

### Added

* **Scan Engine**: Initial folder structure navigation and file counting.
* **Validation**: Added basic error handling for access permissions.

### Improved

* **Formatting**: Enabled alphabetical sorting for scan reports.

> **TL;DR**: The foundation. It can look at a folder and tell you exactly what is inside.

---

## [1.0.0] - 2026-05-15

### Added

* **Initial Release**: Basic path validation and CLI setup.

> **TL;DR**: The first version. It confirms the folder exists and is ready to start working.