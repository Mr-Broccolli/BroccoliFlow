from pathlib import Path
import time

from config import VERSION
from organizer import organize_files
from undo import undo_last_operation
from categories import category_menu

def get_folder():
    while True:
        folder_path = input("\nEnter folder path: ").strip()
        print("\nValidating folder...", end="")
        
        folder = Path(folder_path)

        if folder.exists() and folder.is_dir():
            print(" Done!")
            print(f"\nSelected Folder:\n{folder}")
            return folder

        print(" Error!")
        print("\nInvalid folder path.")

def main():

    print("=" * 40)
    print(f"BroccoliFlow v{VERSION}")
    print("=" * 40)

    while True:

        print("\n1. Organize Files")
        print("2. Undo Last Organization")
        print("3. Manage Categories")
        print("4. Exit")

        option = input(
            "\nSelect Option: "
        ).strip()

        if option == "1":

            folder = get_folder()
            organize_files(folder)

        elif option == "2":

            folder = get_folder()
            undo_last_operation(folder)

        elif option == "3":

            category_menu()

        elif option == "4":

            print("\nGoodbye!")
            break

        else:

            print("\nInvalid option.")
            time.sleep(1)


if __name__ == "__main__":
    main()