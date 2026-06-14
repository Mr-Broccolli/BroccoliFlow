import random
import string
from datetime import datetime
from pathlib import Path

EXTENSIONS = [
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".pdf",
    ".docx",
    ".doc",
    ".txt",
    ".csv",
    ".xlsx",
    ".xls",
    ".pptx",
    ".ppt",
    ".mp4",
    ".mkv",
    ".avi",
    ".mov",
    ".mp3",
    ".wav",
    ".flac",
    ".zip",
    ".7z",
    ".rar",
    ".tar",
    ".gz",
    ".exe",
    ".msi",
]


def generate_dummies():

    print("=" * 40)
    print("BroccoliFlow Test Data Generator")
    print("=" * 40)

    while True:

        try:

            file_count = int(
                input("\nHow many test files would you like to generate? ")
            )
            if file_count > 0:
                break
            print("\nPlease enter a number greater than 0.")
        except ValueError:
            print("\nPlease enter a valid number.")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target_dir = Path(f"test_sandbox_{timestamp}")
    target_dir.mkdir(exist_ok=True)
    print(f"\nGenerating {file_count} dummy files...", end=" ")

    for i in range(file_count):

        extension = random.choice(EXTENSIONS)

        random_name = "".join(
            random.choices(
                string.ascii_lowercase,
                k=8
            )
        )

        filename = (
            target_dir /
            f"test_{random_name}_{i}{extension}"
        )

        with open(filename, "w") as file:

            file.write(
                "DUMMY DATA FOR BROCCOLIFLOW STRESS TEST"
            )

    print("Done!")

    print("\n" + "=" * 40)
    print("GENERATION COMPLETE")
    print("=" * 40)

    print(f"Folder Created : {target_dir.name}")
    print(f"Files Created  : {file_count}")
    print(f"Location       : {target_dir.resolve()}")

    print(
        "\nUse this folder as the target folder in BroccoliFlow "
        "to test scanning, organization, duplicate protection, "
        "and the undo system."
    )


if __name__ == "__main__":
    generate_dummies()