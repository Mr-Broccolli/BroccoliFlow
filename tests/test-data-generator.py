import random
import string
from pathlib import Path

def generate_dummies():
    target_dir = Path("test_sandbox")
    target_dir.mkdir(exist_ok=True)

    extensions = [".png", ".jpg", ".pdf", ".docx", ".mp4", ".mp3", ".zip", ".txt", ".csv", ".exe"]

    print("Generating 500 test files...")

    for i in range(500):
        ext = random.choice(extensions)
        random_name = ''.join(random.choices(string.ascii_lowercase, k=8))
        filename = target_dir / f"test_{random_name}_{i}{ext}"

        with open(filename, "w") as file:
            file.write("DUMMY DATA FOR BROCCOLIFLOW STRESS TEST")

    print(f"Done. Point BroccoliFlow at the '{target_dir.name}' folder.")

if __name__ == "__main__":
    generate_dummies()