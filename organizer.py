import json
import shutil
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List, Tuple
from logger import logger
from categories import load_categories
from utils import get_category, get_available_filename
def organize_files(folder: Path, dry_run: bool = False, max_workers: int = 8) -> None:
    """Organizes files in the specified folder with concurrency and logging."""
    logger.info(f"Starting organization scan on: {folder.absolute()}")
    print(f"\nScanning: {folder}")
    
    files = []
    folders = []
    file_types = Counter()

    try:
        for item in sorted(folder.iterdir(), key=lambda x: x.name.lower()):
            if item.name == "broccoliflow_last_operation.json":
                continue

            if item.is_file():
                files.append(item)
                extension = item.suffix.lower()
                if extension:
                    file_types[extension] += 1
                else:
                    file_types["[no extension]"] += 1
            elif item.is_dir():
                folders.append(item)

    except PermissionError as e:
        logger.error(f"Access denied during scan of {folder}: {e}")
        print("\nAccess denied.")
        print("BroccoliFlow cannot scan this folder.")
        return

    logger.debug(f"Scan found {len(files)} files and {len(folders)} folders.")
    print("\n" + "=" * 40)
    print("SCAN SUMMARY")
    print("=" * 40)
    print(f"Files Found    : {len(files)}")
    print(f"Folders Found  : {len(folders)}")   

    if not files:
        logger.info("Scan complete. No files found to organize.")
        print("\nNo files found to organize.")
        return

    choice = input("\nProceed with organization? (Y/N): ").strip().lower()

    if choice != "y":
        logger.info("User cancelled organization after scan.")
        print("\nOrganization cancelled.")
        return

    category_counts = Counter()
    file_destinations = []
    active_categories = load_categories()
    
    for file in files:
        extension = file.suffix.lower()
        category = get_category(extension, active_categories)
        category_counts[category] += 1 
        destination_folder = folder / category
        file_destinations.append((file, destination_folder))

    if dry_run:
        logger.info("Executing DRY RUN. No files will be modified.")
        print("\n--- DRY RUN MODE: No files will be moved ---")
        for file, dest in file_destinations:
            print(f"[PREVIEW] {file.name} -> {dest.name}/{file.name}")
        return

    print("\nCreating folders...")
    folders_created = 0
    for category in category_counts:
        category_folder = folder / category
        if not category_folder.exists():
            category_folder.mkdir(exist_ok=True)
            logger.debug(f"Created category folder: {category_folder}")
            folders_created += 1

    print("\nMoving files concurrently...")
    logger.info(f"Initiating concurrent transfer for {len(files)} files with {max_workers} workers.")
    moved_files = 0
    renamed_files = 0
    operation_log = []
    
    def process_file(task_data: Tuple[Path, Path]) -> Dict[str, Any]:
        """Worker function for concurrent file processing."""
        source_file, dest_folder = task_data
        original_destination = dest_folder / source_file.name
        final_destination = get_available_filename(original_destination)
        is_renamed = final_destination != original_destination
        try:
            shutil.move(str(source_file), str(final_destination))
            logger.debug(f"Moved: {source_file.name} -> {final_destination.parent.name}/{final_destination.name}")
            return {
                "source": str(source_file),
                "destination": str(final_destination),
                "renamed": is_renamed,
                "error": None
            }
        except Exception as e:
            logger.error(f"Failed to move {source_file.name}: {e}")
            return {
                "source": str(source_file),
                "destination": None,
                "renamed": False,
                "error": str(e)
            }

    try:
        start_move_time = time.time()
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(process_file, task): task for task in file_destinations}

            completed = 0
            for future in as_completed(futures):
                result = future.result()

                if result["error"]:
                    raise RuntimeError(f"Transfer error on {result['source']}: {result['error']}")

                operation_log.append({
                    "source": result["source"],
                    "destination": result["destination"]
                })

                moved_files += 1
                if result["renamed"]:
                    logger.debug(f"Duplicate resolved: {Path(result['source']).name} renamed.")
                    renamed_files += 1

                # Progress reporting
                completed += 1
                if completed % 10 == 0 or completed == len(file_destinations):
                    progress = (completed / len(file_destinations)) * 100
                    print(f"\rProgress: {completed}/{len(file_destinations)} files ({progress:.1f}%)", end="", flush=True)

            # Clear progress line and move to next line
            print()  # New line after progress

        move_time = time.time() - start_move_time
        logger.info(f"Transfer complete in {move_time:.4f} sec.")
        print(f"Transfer Time: {move_time:.4f} sec")
                    
    except Exception as error:
        logger.critical(f"Critical failure during transfer: {error}. Initiating emergency rollback.")
        print(f"\nCritical failure during transfer: {error}")
        print("Initiating emergency rollback...")
        
        rollback_count = 0
        for entry in operation_log:
            if Path(entry["destination"]).exists():
                shutil.move(entry["destination"], entry["source"])
                rollback_count += 1
                
        logger.info(f"Rollback complete. Restored {rollback_count} files to original paths.")
        print("Rollback complete. System state restored.")
        return

    logger.info(f"Organization success: {moved_files} moved, {folders_created} folders created, {renamed_files} duplicates fixed.")

    print("\n" + "=" * 40)
    print("ORGANIZATION REPORT")
    print("=" * 40)

    for category, count in sorted(category_counts.items()):
        print(f"{category:<20} {count}")

    print(f"\nFiles Moved      : {moved_files}")
    print(f"Folders Created  : {folders_created}")
    print(f"Duplicates Fixed : {renamed_files}")

    log_file = folder / "broccoliflow_last_operation.json"
    with open(log_file, "w") as file:
        json.dump(operation_log, file, indent=4)
        logger.debug(f"Operation undo log saved to {log_file}")

    print("\nOrganization complete.")