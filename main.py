from pathlib import Path

print("=" * 40)
print("BroccoliFlow v1.0")
print("=" * 40)

while True:
    folder_path = input("\nEnter folder path: ")

    folder = Path(folder_path)

    if folder.exists() and folder.is_dir():
        print("\nFolder found")
        print(f"\nSelected Folder:\n{folder}")
        break

    print("\nInvalid folder path. Please try again.")