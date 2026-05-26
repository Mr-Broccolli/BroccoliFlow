from pathlib import Path

folder_path = input("Enter folder path: ")

folder = Path(folder_path)

if folder.exists():
    print("Folder found!")
else:
    print("Folder does not exist.")