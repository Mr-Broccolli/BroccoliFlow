from pathlib import Path
import time
from collections import Counter
import shutil
import json

VERSION = "1.5.0"

FILE_CATEGORIES = {
    "Images": [
        ".png", ".jpg", ".jpeg", ".gif",
        ".webp", ".bmp", ".tiff", ".svg",
        ".ico"
    ],

    "Documents": [
        ".pdf", ".doc", ".docx",
        ".txt", ".rtf",
        ".xls", ".xlsx", ".csv",
        ".ppt", ".pptx",
        ".odt", ".ods", ".odp"
    ],

    "Videos": [
        ".mp4", ".mkv", ".avi",
        ".mov", ".wmv", ".flv",
        ".webm", ".m4v"
    ],

    "Audio": [
        ".mp3", ".wav", ".flac",
        ".aac", ".ogg", ".m4a",
        ".wma"
    ],

    "Archives": [
        ".zip", ".rar", ".7z",
        ".tar", ".gz", ".bz2",
        ".xz"
    ],

    "Installation Media": [
        ".exe", ".msi", ".msix",
        ".msixbundle", ".appx",
        ".appxbundle"
    ]
}


def get_category(extension):
    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category

    return "Misc"

def get_available_filename(destination_file):

    if not destination_file.exists():
        return destination_file

    stem = destination_file.stem
    suffix = destination_file.suffix
    parent = destination_file.parent

    counter = 1

    while True:

        new_file = (
            parent /
            f"{stem} ({counter}){suffix}"
        )

        if not new_file.exists():
            return new_file

        counter += 1

def undo_last_operation(folder):

    log_file = folder / "broccoliflow_last_operation.json"

    if not log_file.exists():
        print("\nNo operation log found.")
        return

    with open(log_file, "r") as file:
        operation_log = json.load(file)

    print(f"\nFiles Recorded: {len(operation_log)}")

    confirm = input(
        "\nUndo last organization? (Y/N): "
    ).strip().lower()

    if confirm != "y":
        print("\nUndo cancelled.")
        return

    print("\nRestoring files...", end="")
    time.sleep(1)

    restored_files = 0

    for entry in operation_log:

        source = Path(entry["source"])
        destination = Path(entry["destination"])

        if destination.exists():

            source.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            if source.exists():

                print(
                    f"\nSkipped: {source.name}"
                )
                continue

            shutil.move(
                str(destination),
                str(source)
            )

            restored_files += 1

    print("Done!")

    print("\n" + "=" * 40)
    print("UNDO SUMMARY")
    print("=" * 40)

    print(f"Files Restored : {restored_files}")
    print(
        f"Completed At   : "
        f"{time.strftime('%H:%M:%S')}"
    )
    log_file.unlink()

print("=" * 40)
print(f"BroccoliFlow v{VERSION}")
print("=" * 40)

print("\n1. Organize Files")
print("2. Undo Last Organization")

while True:

    option = input(
        "\nSelect Option (1-2): "
    ).strip()

    if option in ["1", "2"]:
        break

    print("Invalid option.")

while True:
    folder_path = input("\nEnter folder path: ").strip()

    print("\nValidating folder...", end="")
    time.sleep(1)

    folder = Path(folder_path)

    if folder.exists() and folder.is_dir():
        print(" Done!")

        print("\nFolder found.")
        print(f"\nSelected Folder:\n{folder}")

        if option == "2":
            undo_last_operation(folder)
            exit()

        time.sleep(1)
        break

    print("Error!")
    print("\nInvalid folder path. Please try again.")

print("\nScanning folder...", end="")
time.sleep(1)
print(" Done!")

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
    exit()

scan_time = time.time() - start_time

print("\nFolder Structure:\n")

print(f"[ROOT] {folder.name}")

if not files and not folders:
    print("-- [EMPTY FOLDER]")

else:
    for subfolder in folders:
        print(f"|-- [DIR]  {subfolder.name}")

    for file in files:
        print(f"|-- [FILE] {file.name}")

print("\n" + "=" * 40)
print("SCAN SUMMARY")
print("=" * 40)

print(f"Files Found    : {len(files)}")
print(f"Folders Found  : {len(folders)}")
print(f"Total Items    : {len(files) + len(folders)}")
print(f"Scan Time      : {scan_time:.4f} sec")
print(f"Scan completed at: {time.strftime('%H:%M:%S')}")

if file_types:
    print("\nFile Types Detected:")

    for extension, count in sorted(file_types.items()):
        print(f"{extension:<15} {count}")

print("\nBroccoliFlow scan completed.")

if not files:
    print("\nNo files found to organize.")
    exit()

choice = input("\nPreview file organization? (Y/N): ").strip().lower()

if choice == "y":

    print("\n" + "=" * 40)
    print("ORGANIZATION PREVIEW")
    print("=" * 40)

    category_counts = Counter()

    file_destinations = []

    for file in files:

        extension = file.suffix.lower()

        category = get_category(extension)

        category_counts[category] += 1

        destination_folder = folder / category

        file_destinations.append(
            (file, destination_folder)
        )

        print(
            f"{file.name:<35} -> {destination_folder}"
        )

    print("\n" + "=" * 40)
    print("ORGANIZATION SUMMARY")
    print("=" * 40)

    for category, count in sorted(category_counts.items()):
        print(f"{category:<20} {count}")

    print(f"\nTotal Files To Organize: {len(files)}")

    print(
        f"\nWARNING: This operation will move "
        f"{len(files)} file(s)."
    )

    print("\nFolders That Will Be Created:")

    for category in sorted(category_counts):
        print(f"- {category}")

    confirm = input(
        "\nProceed with organization? (Y/N): "
    ).strip().lower()

    if confirm == "y":

        print("\nCreating folders...", end="")
        time.sleep(2)

        folders_created = 0

        for category in category_counts:

            category_folder = folder / category

            if not category_folder.exists():
                category_folder.mkdir(exist_ok=True)
                folders_created += 1

        print("Done!")

        print("\nMoving files...", end="")
        time.sleep(2)

        moved_files = 0
        renamed_files = 0
        operation_log = []

        for file, destination_folder in file_destinations:

            original_destination = (
                destination_folder / file.name
            )

            destination_file = get_available_filename(
                original_destination
            )
            if destination_file != original_destination:
                renamed_files += 1

                print(
                    f"\nDuplicate detected:"
                    f"\n{file.name} -> {destination_file.name}"
                )

            shutil.move(
                str(file),
                str(destination_file)
            )

            operation_log.append({
                "source": str(file),
                "destination": str(destination_file)
            })

            moved_files += 1

        print("Done!")
        time.sleep(1)
        print("\n" + "=" * 40)
        print("ORGANIZATION REPORT")
        print("=" * 40)

        for category, count in sorted(category_counts.items()):
            print(f"{category:<20} {count}")

        print(f"\nFiles Moved      : {moved_files}")
        print(f"Folders Created  : {folders_created}")
        print(f"Duplicates Fixed : {renamed_files}")
        print(f"Completed At     : {time.strftime('%H:%M:%S')}")

        log_file = folder / "broccoliflow_last_operation.json"

        with open(log_file, "w") as file:
           json.dump(
                operation_log,
                file,
                indent=4
            )

        print("\n" + "=" * 40)
        print("ORGANIZATION COMPLETE")
        print("=" * 40)

        print("\nThank you for using BroccoliFlow.")