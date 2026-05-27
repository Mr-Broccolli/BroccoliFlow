from pathlib import Path
import time
from collections import Counter

print("=" * 40)
print("BroccoliFlow v1.1")
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

print(folder.name)

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

if file_types:
    print("\nFile Types Detected:")

    for extension, count in sorted(file_types.items()):
        print(f"{extension:<15} {count}")

print("\nBroccoliFlow scan completed.")