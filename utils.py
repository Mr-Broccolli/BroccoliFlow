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