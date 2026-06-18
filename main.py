import argparse
import sys
from pathlib import Path
from logger import logger, set_debug_level
from organizer import organize_files
from undo import undo_last_operation
from categories import category_menu
from config import VERSION

def run_menu():
    """Main interactive menu logic."""
    logger.info("User entered interactive menu.")
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
                logger.warning(f"User provided invalid path: {folder_path}")
                print("\nInvalid folder path.")
                
        elif option == "2":
            folder_path = input("\nEnter folder path: ").strip()
            folder = Path(folder_path)
            if folder.exists() and folder.is_dir():
                undo_last_operation(folder)
            else:
                logger.warning(f"User provided invalid path for undo: {folder_path}")
                print("\nInvalid folder path.")
                
        elif option == "3":
            category_menu()
            
        elif option == "4":
            logger.info("User exited via menu.")
            print("\nGoodbye!")
            break
            
        else:
            print("\nInvalid option.")

def main():
    """Main application controller."""
    #defining CLI arguments
    parser = argparse.ArgumentParser(description="BroccoliFlow - Automated File Organizer")
    parser.add_argument("--source", type=str, help="Path to the directory to organize")
    parser.add_argument("--organize", action="store_true", help="Run the organization process")
    parser.add_argument("--undo", action="store_true", help="Undo the last organization")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without moving files")
    parser.add_argument("--debug", action="store_true", help="Enable verbose debug logging")

    args = parser.parse_args()

    #toggle debug mode early if requested
    if args.debug:
        set_debug_level(True)
        logger.debug("Debug mode enabled via CLI.")

    logger.info("BroccoliFlow application started.")

    #if CLI arguments are provided, bypass the menu
    if args.source:
        folder = Path(args.source)
        if not folder.exists() or not folder.is_dir():
            logger.error(f"CLI Error: {args.source} is not a valid directory.")
            print(f"Error: {args.source} is not a valid directory.")
            sys.exit(1)

        if args.organize:
            logger.info(f"CLI trigger: Organizing {folder} (Dry Run: {args.dry_run})")
            organize_files(folder, dry_run=args.dry_run)
        elif args.undo:
            logger.info(f"CLI trigger: Undoing {folder}")
            undo_last_operation(folder)
        else:
            print("Error: You provided a source but no action. Use --organize or --undo.")
            sys.exit(1)
        return

    #default to interactive menu if no arguments provided
    try:
        run_menu()
    except KeyboardInterrupt:
        logger.warning("Execution interrupted by user (Ctrl+C).")
        print("\n\nExecution interrupted. Exiting safely. Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()