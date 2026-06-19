import json
from pathlib import Path
from typing import Dict, List
from config import DEFAULT_CATEGORIES

CONFIG_DIR = Path("config")
CONFIG_FILE = CONFIG_DIR / "categories.json"


def _validate_categories(categories: Dict[str, List[str]]) -> bool:
    """Validate categories configuration structure.

    Args:
        categories: Dictionary mapping category names to lists of file extensions

    Returns:
        True if valid, False otherwise
    """
    if not isinstance(categories, dict):
        return False

    for category, extensions in categories.items():
        if not isinstance(category, str):
            return False
        if not isinstance(extensions, list):
            return False
        for ext in extensions:
            if not isinstance(ext, str) or not ext.startswith('.'):
                return False
    return True

def load_categories():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as file:
                categories = json.load(file)
                if _validate_categories(categories):
                    return categories
                else:
                    print("\nInvalid categories.json structure. Using default categories.")
        except json.JSONDecodeError:
            print("\nInvalid categories.json. Using default categories.")

    return DEFAULT_CATEGORIES.copy()

def save_categories(categories):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as file:
        json.dump(categories, file, indent=4)

def view_categories(categories):
    print("\n" + "=" * 40)
    print("CURRENT CATEGORIES")
    print("=" * 40)
    for category, extensions in sorted(categories.items()):
        print(f"\n{category}")
        for extension in extensions:
            print(f"  {extension}")

def create_category(categories):
    print("\nCreate New Category")
    name = input("\nCategory name: ").strip()
    
    if not name:
        print("\nCategory name cannot be empty.")
        return
        
    if name in categories:
        print("\nCategory already exists.")
        return

    extensions = input("\nExtensions (comma separated): ").strip()
    extension_list = []
    
    for extension in extensions.split(","):
        extension = extension.strip().lower()
        if not extension.startswith("."):
            extension = "." + extension
        extension_list.append(extension)

    categories[name] = extension_list
    save_categories(categories)
    print(f"\n{name} created successfully.")

def delete_category(categories):
    if not categories:
        print("\nNo categories found.")
        return

    print("\nCategories:\n")
    category_list = sorted(categories.keys())
    
    for index, category in enumerate(category_list, start=1):
        print(f"{index}. {category}")

    try:
        choice = int(input("\nSelect category: "))
    except ValueError:
        print("\nInvalid selection.")
        return

    if not 1 <= choice <= len(category_list):
        print("\nInvalid selection.")
        return

    category = category_list[choice - 1]
    confirm = input(f"\nDelete '{category}'? (Y/N): ").strip().lower()

    if confirm != "y":
        print("\nDeletion cancelled.")
        return

    del categories[category]
    save_categories(categories)
    print(f"\n{category} deleted.")

def reset_categories(categories):
    if not CONFIG_FILE.exists():
        print("\nAlready using default categories.")
        return

    confirm = input("\nDelete custom configuration? (Y/N): ").strip().lower()
    
    if confirm != "y":
        print("\nReset cancelled.")
        return

    CONFIG_FILE.unlink()
    categories.clear()
    categories.update(DEFAULT_CATEGORIES.copy())
    print("\nDefault categories restored.")

def category_menu():
    categories = load_categories()

    while True:
        print("\n" + "=" * 40)
        print("CATEGORY MANAGER")
        print("=" * 40)
        print("\n1. Create Category")
        print("2. View Categories")
        print("3. Delete Category")
        print("4. Reset Categories")
        print("5. Back")

        choice = input("\nSelect Option: ").strip()

        if choice == "1":
            create_category(categories)
        elif choice == "2":
            view_categories(categories)
        elif choice == "3":
            delete_category(categories)
        elif choice == "4":
            reset_categories(categories)
        elif choice == "5":
            break
        else:
            print("\nInvalid option.")

        input("\nPress Enter to continue...")