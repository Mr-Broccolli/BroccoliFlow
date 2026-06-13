from pathlib import Path
import json
import shutil
import time

def undo_last_operation(folder):

    log_file = folder / "broccoliflow_last_operation.json"

    if not log_file.exists():
        print("\nNo operation log found.")
        return
    try:
        with open(log_file, "r") as file:
            operation_log = json.load(file) 
    except json.JSONDecodeError:
        print("\nOperation log is corrupted.")
        return

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
    skipped_files = 0

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
                skipped_files += 1
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
    print(f"Files Skipped  : {skipped_files}")
    print(
        f"Completed At   : "
        f"{time.strftime('%H:%M:%S')}"
    )
    input(
        "\nPress Enter to continue, or Ctrl+C to exit..."
    )
    if skipped_files == 0:
        log_file.unlink()
