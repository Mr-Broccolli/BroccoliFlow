from config import DEFAULT_CATEGORIES
from pathlib import Path
from typing import Dict, List
import sys


def get_category(extension: str, active_categories: Dict[str, List[str]]) -> str:
    for category, extensions in active_categories.items():
        if extension in extensions:
            return category

    return "Misc"


def get_available_filename(destination_file: Path) -> Path:
    if not destination_file.exists():
        return destination_file

    stem = destination_file.stem
    suffix = destination_file.suffix
    parent = destination_file.parent

    counter = 1

    while True:
        new_file = parent / f"{stem} ({counter}){suffix}"

        if not new_file.exists():
            return new_file

        counter += 1


def _get_forbidden_prefixes() -> list[Path]:
    """Return list of system directory prefixes that should never be organized."""
    if sys.platform == "win32":
        system_root = Path.home().drive + "\\"
        return [
            Path(system_root) / "Windows",
            Path(system_root) / "Program Files",
            Path(system_root) / "Program Files (x86)",
            Path(system_root) / "System Volume Information",
        ]
    return [
        Path("/etc"),
        Path("/usr"),
        Path("/bin"),
        Path("/sbin"),
        Path("/lib"),
        Path("/lib64"),
        Path("/boot"),
        Path("/root"),
        Path("/var"),
        Path("/sys"),
        Path("/proc"),
    ]


def validate_source_path(path: Path) -> None:
    """Validate source path is safe for organization.

    Raises:
        ValueError: If path contains traversal attempts or resolves to system directory.
    """
    if ".." in str(path):
        raise ValueError("Path traversal attempts (..) are not allowed")

    resolved = path.resolve()

    for forbidden in _get_forbidden_prefixes():
        try:
            if resolved.is_relative_to(forbidden):
                raise ValueError(f"Path resolves to system directory: {forbidden}")
        except (ValueError, OSError):
            continue