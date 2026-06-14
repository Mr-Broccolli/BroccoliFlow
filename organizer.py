from collections import Counter
from categories import load_categories
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import shutil
import time

from utils import get_category, get_available_filename

def organize_files(folder):
    print("\nScanning folder...")
    start_time = time.time()

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

    except PermissionError:
        print("\nAccess denied.")
        print("BroccoliFlow cannot scan this folder.")
        return

    scan_time = time.time() - start_time

    print("\n" + "=" * 40)
    print("SCAN SUMMARY")
    print("=" * 40)
    print(f"Files Found    : {len(files)}")
    print(f"Folders Found  : {len(folders)}")
    print(f"Scan Time      : {scan_time:.4f} sec")

    if not files:
        print("\nNo files found to organize.")
        return

    choice = input("\nProceed with organization? (Y/N): ").strip().lower()

    if choice != "y":
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

    print("\nCreating folders...")
    folders_created = 0
    for category in category_counts:
        category_folder = folder / category
        if not category_folder.exists():
            category_folder.mkdir(exist_ok=True)
            folders_created += 1

    print("\nMoving files concurrently...")
    
    moved_files = 0
    renamed_files = 0
    operation_log = []
    
    def process_file(task_data):
        source_file, dest_folder = task_data
        original_destination = dest_folder / source_file.name
        final_destination = get_available_filename(original_destination)
        is_renamed = final_destination != original_destination
        
        shutil.move(str(source_file), str(final_destination))
        
        return {
            "source": str(source_file),
            "destination": str(final_destination),
            "renamed": is_renamed
        }

    try:
        start_move_time = time.time()
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = {executor.submit(process_file, task): task for task in file_destinations}
            
            for future in as_completed(futures):
                result = future.result()
                operation_log.append({
                    "source": result["source"],
                    "destination": result["destination"]
                })
                
                moved_files += 1
                if result["renamed"]:
                    renamed_files += 1
        move_time = time.time() - start_move_time
        print(f"Transfer Time: {move_time:.4f} sec")
                    
    except Exception as error:
        print(f"\nCritical failure during transfer: {error}")
        print("Initiating emergency rollback...")
        
        for entry in operation_log:
            if Path(entry["destination"]).exists():
                shutil.move(entry["destination"], entry["source"])
                
        print("Rollback complete. System state restored.")
        return

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

    print("\nOrganization complete.")