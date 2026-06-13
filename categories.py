import json
from pathlib import Path

from config import DEFAULT_CATEGORIES

CONFIG_FILE = Path("categories.json")


def load_categories():
    """Load custom categories if available."""

    if CONFIG_FILE.exists():

        try:
            with open(CONFIG_FILE, "r") as file:
                return json.load(file)

        except json.JSONDecodeError:

            print("\nInvalid categories.json.")
            print("Using default categories.")

    return DEFAULT_CATEGORIES.copy()


def save_categories(categories):

    with open(CONFIG_FILE, "w") as file:
        json.dump(
            categories,
            file,
            indent=4
        )


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

    name = input(
        "\nCategory name: "
    ).strip()

    if not name:

        print("\nCategory name cannot be empty.")
        return

    if name in categories:

        print("\nCategory already exists.")
        return

    extensions = input(
        "\nExtensions (comma separated): "
    ).strip()

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

        choice = int(
            input("\nSelect category: ")
        )

    except ValueError:

        print("\nInvalid selection.")
        return

    if not 1 <= choice <= len(category_list):

        print("\nInvalid selection.")
        return

    category = category_list[choice - 1]

    confirm = input(
        f"\nDelete '{category}'? (Y/N): "
    ).strip().lower()

    if confirm != "y":

        print("\nDeletion cancelled.")
        return

    del categories[category]

    save_categories(categories)

    print(f"\n{category} deleted.")


def reset_categories():

    if not CONFIG_FILE.exists():

        print("\nAlready using default categories.")
        return

    confirm = input(
        "\nDelete custom configuration? (Y/N): "
    ).strip().lower()

    if confirm != "y":

        print("\nReset cancelled.")
        return

    CONFIG_FILE.unlink()

    print("\nDefault categories restored.")


def category_menu():

    while True:

        categories = load_categories()

        print("\n" + "=" * 40)
        print("CATEGORY MANAGER")
        print("=" * 40)

        print("\n1. Create Category")
        print("2. View Categories")
        print("3. Delete Category")
        print("4. Reset Categories")
        print("5. Back")

        choice = input(
            "\nSelect Option: "
        ).strip()

        if choice == "1":

            create_category(categories)

        elif choice == "2":

            view_categories(categories)

        elif choice == "3":

            delete_category(categories)

        elif choice == "4":

            reset_categories()

        elif choice == "5":

            break

        else:

            print("\nInvalid option.")

        input("\nPress Enter to continue...")