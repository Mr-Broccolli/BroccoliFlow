# PROJECT_MEMORY.md

## 1. Project Identity

**Project Name:** BroccoliFlow
**Current Version:** 1.8.0 (defined in config.py)
**Target Operating Systems:** Cross-platform (Windows, macOS, Linux). Heavily tested on Windows.
**Programming Language:** Python 3.9+ (uses built-in generic types like `list`, `dict`, `tuple` from typing module)
**Dependencies:** Zero external dependencies. Strictly Python Standard Library.
**Philosophy:** Automated, fast, and bulletproof. The tool must never corrupt user data, must fail gracefully, and must leave an exact audit trail of everything it does.
**Target Users:** Power users, developers, and data hoarders who need automated file organization without the bloat of GUI-first applications.
**Vision:** The ultimate high-performance CLI toolkit for local filesystem management.
**Versioning Strategy:** Semantic Versioning (SemVer).
**Repository Structure:** Flat monolithic structure for core files. `logs/` directory created at runtime (gitignored). `tests/` directory for testing utilities.
**Release Strategy:** Feature-driven releases. v1.7.0 hit the 100-commit milestone.

## 2. Complete Architecture

The codebase is modular and strictly separates the UI (CLI/Menu) from the business logic (File Operations).

### `main.py`
**Purpose:** Application entry point and routing controller.
**Responsibilities:** Parses command-line arguments using `argparse`. Falls back to an interactive terminal menu if no arguments are provided. Catches top-level exceptions like `KeyboardInterrupt`.
**Inputs:** `sys.argv` (CLI flags), `stdin` (interactive menu).
**Outputs:** Routes execution to `organizer.py` or `undo.py`.
**Imports:** `argparse`, `sys`, `pathlib.Path`, `logger`, `organizer`, `undo`, `categories`, `config`.
**Future Growth:** Will become entirely CLI-focused as the interactive menu is phased out.

### `organizer.py`
**Purpose:** The core execution engine.
**Responsibilities:** Scans target directories, counts file types, creates missing category folders, dispatches file move operations to a thread pool, logs operations to a JSON file, and orchestrates emergency rollbacks if transfers fail.
**Inputs:** Target `Path` object, `dry_run` boolean, `max_workers` integer.
**Outputs:** Moves physical files. Writes `broccoliflow_last_operation.json` to the target folder.
**Imports:** `json`, `shutil`, `time`, `collections.Counter`, `concurrent.futures.ThreadPoolExecutor`, `pathlib.Path`, `logger`, `categories`, `utils`.
**Global Variables:** None. Pure functions driven by state passed as arguments.
**Reason for Existence:** Isolates dangerous filesystem mutations from user input logic.

### `logger.py`
**Purpose:** Global telemetry and observability.
**Responsibilities:** Configures the Python `logging` module. Prevents duplicate log handlers. Sets up persistent file writer to `logs/broccoliflow.log` with rotation (5 MB per file, 5 backups). Exposes a function to dynamically swap between `INFO` and `DEBUG` levels.
**Inputs:** `debug` boolean flag.
**Outputs:** Writes formatted strings to disk.
**Imports:** `logging`, `logging.handlers`, `pathlib.Path`.
**Reason for Existence:** Tracing crashes in threaded environments is impossible with standard print statements. A permanent black-box recorder is required.

### `undo.py`
**Purpose:** The time machine.
**Responsibilities:** Reads `broccoliflow_last_operation.json`, verifies file existence, and moves files back to their original paths.
**Inputs:** Target `Path` object.
**Outputs:** Reverses filesystem mutations.
**Reason for Existence:** Trust. Users will not run an automated tool if they cannot reverse a mistake.

### `categories.py`
**Purpose:** Configuration management.
**Responsibilities:** Loads `config/categories.json` into memory. Provides a fallback dictionary if the file is missing or invalid. Contains logic for the interactive category manager menu. Validates configuration structure on load.
**Inputs:** Reads `config/categories.json`.
**Outputs:** Returns dictionary mappings of extensions to folder names.

### `utils.py`
**Purpose:** Stateless helper functions.
**Responsibilities:** Houses `get_category()` for extension matching and `get_available_filename()` for duplicate collision protection.
**Inputs:** Strings and Paths.
**Outputs:** Strings and Paths.
**Reason for Existence:** Keeps `organizer.py` clean.

### `config.py`
**Purpose:** Global constants.
**Responsibilities:** Stores `VERSION = "1.8.0"`. Defines `DEFAULT_CATEGORIES` dictionary mapping categories to extension lists.

### `config/categories.json`
**Purpose:** User-configurable schema mapping extensions (like `.jpg`) to target folders (like `Images`).
**Behavior:** Created on first run if missing. Validated on every load. Falls back to `DEFAULT_CATEGORIES` if malformed.

## 3. Complete Development Timeline

### v1.0.0 to v1.6.0 (The Script Era)
- Started as a basic procedural script.
- Added an interactive terminal menu for ease of use.
- Implemented `categories.json` so hardcoded sorting rules were removed.
- Built the initial `undo.py` feature using a basic JSON log.
- Problems encountered: The script was slow for large directories. Terminal menus made automation impossible.

### v1.7.0 (The Architecture Refactor) — 2026-06-16
- Features: Introduced `argparse` CLI flags (`--source`, `--organize`, `--undo`, `--dry-run`).
- Architecture changes: Ripped the interactive menu out of the core logic. Separated into `main.py` and `organizer.py`.
- Performance: Replaced sequential file moving with `concurrent.futures.ThreadPoolExecutor`. Added atomic rollbacks to catch thread crashes.
- Milestone: Reached 100 commits.

### v1.8.0 (The Observability Update) — 2026-06-20
- Features: Replaced `print()` debugging with the Python `logging` module. Added persistent file logging to `logs/broccoliflow.log` with rotation (5 MB, 5 backups). Added `--debug` CLI flag for console debug output. Added `--max-workers` flag for adjustable parallelism. Added `--version` flag. Improved help strings. Added `KeyboardInterrupt` handling for clean Ctrl+C exits. Added real-time progress reporting (updates every 10 files). Added configuration validation with fallback to defaults.
- Refactors: Passed global logger instances across modules to prevent double-logging. Added type hints across all modules.
- Why: Multi-threaded file operations fail silently or create race conditions. A definitive audit trail was needed.

## 4. Complete Roadmap

### Implemented
- Threaded file organization.
- CLI automation.
- Atomic rollbacks.
- Persistent log rotation.
- Duplicate filename protection.
- Configuration validation with fallback.
- Progress reporting.
- Type hints across codebase.

### In Progress (Targeting v1.9.0 - Sanity & Resilience)
- Runtime Environment Checks. Verify read/write permissions before spinning up threads.
- Graceful Recovery. Implement a wait-and-retry decorator for `PermissionError` on locked files.
- Path Traversal Protection. Ensure users cannot pass relative paths like `../../Windows/System32` into the source argument.

### Planned (Targeting v2.0.0+)
- Recursive subfolder scanning using `Path.rglob()`.
- Graphical User Interface (GUI) wrapper over the CLI architecture.

### Rejected Ideas
- Partial file recovery on crash. (Rejected because leaving a folder in a half-sorted state is a nightmare. Atomic rollback is safer).
- Deleting files. (Permanently abandoned. BroccoliFlow only moves files. Deletion introduces catastrophic risk).

## 5. Feature Documentation

### Concurrent Transfer Engine
**Workflow:** `organizer.py` builds a list of source/destination tuples. It feeds these to a `ThreadPoolExecutor` with `max_workers=8` (configurable via `--max-workers`). `as_completed()` yields results as they finish.
**Limitations:** Bound by disk I/O, not CPU. Increasing workers past 8 on spinning hard drives actually degrades performance.
**Failure Cases:** If a thread throws an unhandled exception (like disk full), the main thread catches it, kills the remaining tasks, and loops over `operation_log` to reverse everything.

### Duplicate Protection
**Workflow:** `utils.get_available_filename(path)` checks if a file exists at the destination.
**Internal Logic:** If `image.jpg` exists, it tests `image (1).jpg`, `image (2).jpg` inside a `while` loop until it finds free space.

### Operation Logging (Undo)
**Workflow:** As threads succeed, they append their move data to an in-memory list.
**Implementation:** Once the pool finishes, this list is dumped to `broccoliflow_last_operation.json` in the target directory.
**Edge Cases:** If the user moves this JSON file manually, the undo command fails.

### Dry Run Mode
**Workflow:** User passes `--dry-run`.
**Implementation:** The script builds the destination list and prints the intended moves to the console, but immediately returns before creating folders or spawning threads.

## 6. Internal Architecture Decisions

- **Why `ThreadPoolExecutor`?** `asyncio` is great for network-bound tasks, but `shutil.move` is a blocking I/O operation. Threads are the correct native Python tool for overlapping disk I/O waits.
- **Why `pathlib`?** `os.path` is archaic. `pathlib` provides an object-oriented approach that makes path concatenation (`folder / category`) and suffix extraction (`file.suffix`) completely foolproof across different operating systems.
- **Why JSON for undo logs?** SQLite is overkill. CSV is ugly. JSON maps perfectly to Python dictionaries and is human-readable if a user needs to manually inspect what happened.
- **Why CLI before GUI?** A robust CLI forces you to decouple UI from business logic. A GUI is just a different way to pass string arguments to a CLI engine.
- **Why rollback instead of partial recovery?** Data integrity is paramount. If a 1000-file transfer fails at file 500, the user has no idea what moved and what did not. Reverting everything to the original state gives the user a clean slate to fix the problem and try again.

## 7. Complete File Structure

```text
BroccoliFlow/
├── config/
│   └── categories.json            (Generated at runtime, user-editable)
├── logs/
│   └── broccoliflow.log           (Generated: Persistent audit trail with rotation)
├── tests/
│   ├── test-data-generator.py     (Generates dummy files for testing)
│   └── README.md                  (Test utility documentation)
├── assets/
│   └── screenshots/               (Release screenshots)
├── main.py                        (Core: CLI and execution routing)
├── organizer.py                   (Core: File transfer and thread management)
├── logger.py                      (Core: Observability configuration)
├── undo.py                        (Core: Reverses operations)
├── categories.py                  (Core: JSON config parsing and validation)
├── utils.py                       (Core: Stateless string/path helpers)
├── config.py                      (Core: Versioning constants and defaults)
├── AGENTS.md                      (Meta: AI working rules)
├── PROJECT_MEMORY.md              (Meta: This document)
├── CHANGELOG.md                   (Meta: Version history)
├── README.md                      (Meta: Public documentation)
├── LICENSE                        (Meta: MIT License)
├── requirements.txt               (Meta: Zero dependencies)
└── .gitignore                     (Meta: Ignore venv, pycache, logs, test sandboxes)
```

## 8. Coding Standards

- **Imports:** Standard library first, third-party second, local modules third. Absolute imports preferred.
- **Typing:** Type hints on all public functions. Uses built-in generics (`list`, `dict`, `tuple`) requiring Python 3.9+.
- **Formatting:** PEP8 compliant. 4 spaces for indentation.
- **Error Handling:** Never use bare `except:`. Always catch specific exceptions (`PermissionError`, `JSONDecodeError`). If catching a generic `Exception`, it must be logged immediately with stack context.
- **String Formatting:** Strictly use f-strings.
- **Logging vs Printing:** `print()` is exclusively for terminal UI elements (menus, final reports). `logger.info()` or `logger.debug()` is exclusively for system events. Never mix them.
- **Forbidden APIs:** `os.system()`, `subprocess` (unless absolutely necessary for a non-Python task), and `os.path`.

## 9. User Preferences

**Identity:** The human developer is Nemo, a 12th class ISC board student aiming for a B.Tech CSE with a specialization in Gaming Technology or animation.

**Tone:** You must be cynical, sarcastic, chatty, and completely informal. Be chill. Be a ruthless mentor. If Nemo's ideas are garbage, say so immediately. Stress test everything. Do not coddle.

**Language:** Clear, simple language. Informative. Active voice exclusively. Avoid passive voice. Address the user directly with "you" and "your".

**Banned Syntax in text:** Do not use em dashes (use parentheses or separate sentences). Do not use constructions like "...not just this, but also this". Do not use cliches or generalizations. Do not use setup language like "in conclusion", "in closing", "additionally", or "furthermore". Cut the fluff and unnecessary adjectives.

**Workflow:** Nemo wants forward-thinking, innovative, out-of-the-box solutions. Act like a professional. Do not avoid risks.

**Command:** Always do as Nemo says. Do not say anything useless. Get straight to the task.

## 10. AI Assistant Directives

**Rule 1:** Read this document completely before proposing any architectural change.

**Rule 2:** You must write code that strictly separates the UI (`main.py`) from business logic (`organizer.py`).

**Rule 3:** Update the AGENTS.md document immediately after implementing a feature.

**Rule 4:** Adopt the persona outlined in Section 9. Be a ruthless, sarcastic mentor. Correct Nemo sharply if they introduce bad practices.

**Rule 5:** Provide complete, rewritten files when providing code. Do not output snippet patches that force the user to guess where things go.

**Rule 6:** Treat security, data integrity, and observability as non-negotiable requirements for every new feature.

## 11. Testing Infrastructure

**Current State:** Fully manual.

**Dummy Generators:** `tests/test-data-generator.py` creates a timestamped `test_sandbox_YYYYMMDD_HHMMSS` folder with N randomly named files across supported extensions.

**Future Plans:** Implement a `tests/` directory with pytest. Need a `generate_dummy_files.py` script that creates 10,000+ empty files with random extensions to stress test the `ThreadPoolExecutor`.

**Failure Injection:** Need a way to mock a `PermissionError` midway through a transfer to properly test the emergency rollback logic in an automated pipeline.

## 12. Git Workflow

**Branching:** Currently developing directly on `main`. Feature branches exist on remote (`feature/custom-categories`, `feature/duplicate-protection`, `feature/logging`, `feature/terminal-flags`) but have been merged.

**Commits:** Standardize on conventional commits (`feat:`, `fix:`, `refactor:`).

**Milestones:** v1.7.0 hit 100 commits.

**Versioning:** Update `config.py` VERSION variable before cutting a release.

## 13. Known Bugs

**The JSON Bomb:** If `categories.json` is manually edited by the user and they miss a comma, the app crashes on startup. (Partially fixed in v1.8.0 via `_validate_categories` in `categories.py` which falls back to defaults with a warning. However, the validation only runs on load, not on save).

**Locked File Crash:** If another application is actively writing to a file (like a downloading video), `shutil.move` throws a `PermissionError` and triggers an immediate rollback. It needs retry logic with exponential backoff.

**Orphaned Log Files:** If a user moves `broccoliflow_last_operation.json` manually out of the directory, they lose the ability to undo.

**Progress Reporting Race Condition:** Progress counter increments in the main thread after `as_completed`, but if an exception occurs mid-transfer, the progress line may not clean up properly.

## 14. Performance

**Bottlenecks:** Disk I/O. `ThreadPoolExecutor` helps, but ultimately a 5400RPM hard drive will choke on thousands of files.

**Memory Usage:** Very low. We only hold lists of file paths in memory, not the file contents.

**Threading Limit:** Configurable via `--max-workers` (default 8). Should ideally detect CPU core count using `os.cpu_count()` and scale dynamically, but bound it to a reasonable maximum to avoid thrashing the disk.

## 15. Security

**Path Traversal:** Need to ensure users cannot pass relative paths like `../../Windows/System32` into the source argument and accidentally nuke system directories. Currently not implemented.

**Atomicity:** The rollback system handles logical atomicity, but physical disk corruption (power loss during `shutil.move`) is still a risk. We rely on the OS filesystem journal to handle hardware-level corruption.

## 16. Future Ideas

**Schema Validator:** A startup check that confirms `categories.json` is a valid dictionary containing only lists of strings. (Partially implemented in v1.8.0 via `_validate_categories`).

**Wait-and-Retry Decorator:** A wrapper around `shutil.move` that pauses for 500ms and retries if it hits an OS lock. Priority is high.

**Recursive Scanning:** Allowing users to organize highly nested folders. Priority is medium. It requires careful handling to avoid infinite recursion on symlinks.

## 17. Current Conversation Dump

We completed v1.7.0 by decoupling the CLI from the interactive menu. We set up argparse with `--source`, `--organize`, `--undo`, `--dry-run`.

We completed v1.8.0 by ripping out `print()` statements from `organizer.py` and replacing them with `logger.info()` and `logger.debug()`.

We created `logger.py` to handle persistent logging to `logs/broccoliflow.log`. We implemented a check (`if not logger.handlers:`) to ensure log lines aren't duplicated.

We built a dynamic level switcher (`set_debug_level`) so the CLI `--debug` flag can turn on verbose logging without re-initializing the entire logger.

We finalized the code for `main.py`, `logger.py`, and `organizer.py`. The code is clean, threaded, and atomic.

We decided the next move is v1.9.0, focusing strictly on stability. Specifically, we will build runtime permission checks, path traversal protection, and a wait-and-retry decorator for locked files.

We discussed moving from web LLMs to OpenCode (local desktop LLM) to maintain context window control.

## 18. Complete Context Preservation

This document contains everything. Every decision, architecture setup, bug, and future roadmap item has been written here directly. You do not need any hidden chat history. You are fully equipped to read the current .py files in the workspace, cross-reference them with this document, and immediately begin building the resilience features for v1.9.0. Do not ask for previous context. Act on this document alone.

## 19. Glossary of Important Terminology

- **Operation Log:** The `broccoliflow_last_operation.json` file written to the target directory after a successful organization run. Contains a list of `{"source": "...", "destination": "..."}` objects.
- **Dry Run:** A simulation mode that prints intended file movements without modifying the filesystem.
- **Atomic Rollback:** The emergency reversal of all file moves if any single transfer fails during the concurrent execution phase.
- **Category:** A folder name (e.g., "Images") mapped to a list of file extensions (e.g., `[".jpg", ".png"]`).
- **Misc:** The fallback category for files with extensions not defined in any category.
- **Worker Thread:** A thread from the `ThreadPoolExecutor` pool that executes `shutil.move` operations.
- **Progress Reporting:** Console output showing `Progress: X/Y files (Z%)` updated every 10 completions.
- **Log Rotation:** Automatic archiving of `broccoliflow.log` when it exceeds 5 MB, keeping up to 5 backup files.