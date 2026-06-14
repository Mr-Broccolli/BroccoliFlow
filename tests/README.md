# BroccoliFlow Test

This folder contains testing utilities for BroccoliFlow.

Its purpose is to help you safely test BroccoliFlow's scanning, organization, duplicate protection, and undo features without using your personal files.

---

## Folder Structure

```text
tests/
├── test-data-generator.py
└── README.md
```

---

## Test Data Generator

The file **`test-data-generator.py`** generates a fresh testing environment filled with randomly named dummy files.

When executed, the generator will:

* Ask how many test files to create.
* Create a new folder named **`test_sandbox`** with a timestamp.
* Generate the requested number of randomly named files.
* Populate the folder with files of various supported extensions.

Supported file types include:

* Images
* Documents
* Videos
* Audio
* Archives
* Installation Media
* Miscellaneous files

The generated files contain only placeholder text and are completely safe to move, rename, organize, and delete.

---

## How to Use

1. Open a terminal in the `tests` folder.
2. Run:

```bash
python test-data-generator.py
```

3. Enter the number of files you want to generate.
4. A new `test_sandbox` folder will be created automatically.
5. Launch BroccoliFlow and select the generated `test_sandbox` folder.
6. Test the following features:

   * Folder scanning
   * File analysis
   * Automatic organization
   * Duplicate filename protection
   * Undo Last Organization

After testing, you can simply delete the `test_sandbox` folder and run the generator again to create a completely new testing environment.

---

## Why This Exists

Testing file organization software on real folders can be risky.

This utility provides a safe environment where you can:

* Verify BroccoliFlow's behavior.
* Stress test with hundreds or thousands of files.
* Test new features before releasing them.
* Debug issues without affecting personal data.

---

## Notes

* The generated files are dummy files and contain no meaningful data.
* File contents are not important. BroccoliFlow organizes files based on their extensions.
* The generator can be run as many times as needed.
* Existing `test_sandbox` folders should be deleted before generating a new one.