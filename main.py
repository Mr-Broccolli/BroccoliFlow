from pathlib import Path
import time
from collections import Counter

FILE_CATEGORIES = {
    "Images": [".png", ".jpg", ".jpeg", ".gif", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".xls"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Audio": [".mp3", ".wav", ".flac"]
}


def get_category(extension):
    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category

    return "Misc"


print("=" * 40)
print("BroccoliFlow v1.2")
print("=" * 40)

while True:
    folder_path = input("\nEnter folder path: ").strip()

    print("\nValidating folder...", end="")
    time.sleep(1)

    folder = Path(folder_path)

    if folder.exists() and folder.is_dir():
        print(" Done!")

        print("\nFolder found.")
        print(f"\nSelected Folder:\n{folder}")

        time.sleep(1)
        break

    print(" Error!")
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
    print("└── [EMPTY FOLDER]")

else:
    for subfolder in folders:
        print(f"├── [DIR]  {subfolder.name}")

    for file in files:
        print(f"├── [FILE] {file.name}")

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

choice = input("\nPreview file organization? (Y/N): ").strip().lower()

if choice == "y":

    print("\n" + "=" * 40)
    print("ORGANIZATION PREVIEW")
    print("=" * 40)

    category_counts = Counter()

    for file in files:

        extension = file.suffix.lower()

        category = get_category(extension)

        category_counts[category] += 1

        print(f"{file.name:<35} -> {category}")

    print("\n" + "=" * 40)
    print("ORGANIZATION SUMMARY")
    print("=" * 40)

    for category, count in sorted(category_counts.items()):
        print(f"{category:<15} {count}")

    print(f"\nTotal Files To Organize: {len(files)}")