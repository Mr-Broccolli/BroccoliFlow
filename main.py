import argparse
from logger import logger 
from pathlib import Path
from organizer import organize_files
from undo import undo_last_operation
from categories import category_menu
from config import VERSION

def run_menu():
    """Main interactive menu logic."""
    print("=" * 40)
    print(f"BroccoliFlow v{VERSION}")
    print("=" * 40)

    while True:
        print("\n1. Organize Files")
        print("2. Undo Last Organization")
        print("3. Manage Categories")
        print("4. Exit")

        option = input("\nSelect Option: ").strip()

        if option == "1":
            folder_path = input("\nEnter folder path: ").strip()
            folder = Path(folder_path)
            if folder.exists() and folder.is_dir():
                organize_files(folder)
            else:
                print("\nInvalid folder path.")
        elif option == "2":
            folder_path = input("\nEnter folder path: ").strip()
            folder = Path(folder_path)
            if folder.exists() and folder.is_dir():
                undo_last_operation(folder)
            else:
                print("\nInvalid folder path.")
        elif option == "3":
            category_menu()
        elif option == "4":
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid option.")

def main():
    logger.info("BroccoliFlow started.")
    """Main application controller."""
    parser = argparse.ArgumentParser(description="BroccoliFlow - Automated File Organizer")
    
    #defining CLI arguments
    parser.add_argument("--source", type=str, help="Path to the directory to organize")
    parser.add_argument("--organize", action="store_true", help="Run the organization process")
    parser.add_argument("--undo", action="store_true", help="Undo the last organization")
    #v1.8.0 placeholder
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without moving files")

    args = parser.parse_args()

    #if CLI arguments are provided, bypass the menu
    if args.source:
        folder = Path(args.source)
        if not folder.exists() or not folder.is_dir():
            print(f"Error: {args.source} is not a valid directory.")
            return

        if args.organize:
            organize_files(folder, dry_run=args.dry_run)
        elif args.undo:
            undo_last_operation(folder)
        return

    #default to interactive menu if no arguments provided
    try:
        run_menu()
    except KeyboardInterrupt:
        print("\n\nExecution interrupted. Exiting safely. Goodbye!")

if __name__ == "__main__":
    main()