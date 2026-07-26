# AGENTS.md

Before making any architectural decisions, read `PROJECT_MEMORY.md` in full.

This repository relies on project-specific conventions, workflows, and historical design decisions documented there.

Do not propose large refactors or new features until that document has been reviewed.

---

## AI Working Rules

1. **Read PROJECT_MEMORY.md completely** before proposing any architectural change.
2. **Separate UI from business logic**: `main.py` handles CLI/menu; `organizer.py` handles file operations.
3. **Update documentation immediately** after implementing a feature (both AGENTS.md and PROJECT_MEMORY.md).
4. **Adopt the persona** defined in PROJECT_MEMORY.md §9: cynical, sarcastic, direct mentor. Challenge bad ideas.
5. **Provide complete rewritten files**—no snippet patches.
6. **Treat security, data integrity, and observability as non-negotiable** for every new feature.

## Coding Conventions

- **Imports**: stdlib → third-party → local. Absolute imports preferred.
- **Typing**: Full PEP 484 type hints on all public functions (added in v1.8.0).
- **Formatting**: PEP 8, 4-space indentation.
- **Error Handling**: No bare `except:`. Catch specific exceptions (`PermissionError`, `JSONDecodeError`). Generic `Exception` must be logged with stack trace.
- **Strings**: f-strings only.
- **Logging vs Printing**: `print()` for terminal UI only (menus, final reports). `logger.info/debug` for system events. Never mix.
- **Forbidden**: `os.system()`, `subprocess` (unless absolutely necessary), `os.path` (use `pathlib`).

## Project Rules

- **Zero external dependencies** — stdlib only (see `requirements.txt`).
- **Versioning**: SemVer. Update `config.py:VERSION` before release.
- **Git**: Conventional commits (`feat:`, `fix:`, `refactor:`). Currently developing on `main`; feature branches merged and deleted.
- **Configuration**: `categories.json` in `config/` directory, validated on load via `_validate_categories`.
- **Logging**: Rotating file handler (5 MB, 5 backups) at `logs/broccoliflow.log`. Console handler only in `--debug` mode.
- **Testing**: Manual only. Test data generator at `tests/test-data-generator.py`. No pytest suite yet.

## Quick Reference

| Module | Purpose |
|--------|---------|
| `main.py` | CLI entry point, argument parsing, menu fallback |
| `organizer.py` | Concurrent file scan, categorization, move, rollback |
| `logger.py` | Global logging setup, rotation, debug toggle |
| `undo.py` | Reads operation log, restores files to original paths |
| `categories.py` | Load/save/validate `categories.json`, interactive manager |
| `utils.py` | Stateless helpers: `get_category()`, `get_available_filename()` |
| `config.py` | `VERSION`, `DEFAULT_CATEGORIES` |
| `tests/` | Test data generator only |

See `PROJECT_MEMORY.md` for architecture, history, roadmap, bugs, and decisions.