import os
import shutil
import hashlib
import sys


def display_signature_progress(completion, total, bar_width=10):
    bar_slots = "🍒🍋🔔💰🚁🛩️🛸🚀🛰️"
    drone_str = "DRONE2MAX!"
    slots_filled = int((completion / total) * bar_width)
    bar_str = drone_str[:slots_filled] + bar_slots[
        ((completion % len(bar_slots)) - 1) % len(bar_slots)
    ] * (bar_width - slots_filled)
    bar_str = bar_str[:bar_width]

    sys.stdout.write(f"\r[{bar_str}] {completion}/{total} completed")
    sys.stdout.flush()


def ensure_directory_exists(path: str) -> None:
    """Ensure the target directory exists; create it if it doesn't."""
    if not os.path.exists(path):
        os.makedirs(path)


def generate_file_hash(file_path: str) -> str:
    """Generate a SHA-256 hash for the content of the given file."""
    hash_obj = hashlib.sha256()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()


def files_are_different(source_file: str, target_file: str) -> bool:
    """Determine if two files differ based on their content's hash."""
    return generate_file_hash(source_file) != generate_file_hash(target_file)


def get_unique_file_name(directory: str, file_name: str) -> str:
    """Generate a unique file name within the specified directory by appending a counter to the file name."""
    base_name, extension = os.path.splitext(file_name)
    counter = 1
    new_file_name = file_name
    while os.path.exists(os.path.join(directory, new_file_name)):
        new_file_name = f"{base_name}_({counter}){extension}"
        counter += 1
    return new_file_name


def move_and_deduplicate_files(source_dir: str, target_dir: str) -> None:
    """Move files from source to target directory, renaming to avoid overwrites and skipping identical content."""
    ensure_directory_exists(target_dir)
    for subdir, _, files in os.walk(source_dir):
        display_signature_progress(subdir, source_dir, 10)
        for file in files:
            source_file_path = os.path.join(subdir, file)
            target_file_path = os.path.join(target_dir, file)

            if os.path.exists(target_file_path):
                if files_are_different(source_file_path, target_file_path):
                    unique_file_name = get_unique_file_name(target_dir, file)
                    target_file_path = os.path.join(target_dir, unique_file_name)
                else:
                    print(
                        f"Skipped '{file}' as identical content exists in the target directory."
                    )
                    continue
            shutil.move(source_file_path, target_file_path)
    print("All files have been processed.")


# Configuration
source_dir = r".\Genera_of_Pinopsida_raw"
target_dir = r".\Dataset\Pinopsida\images2"

# Execute the function to move and deduplicate files
move_and_deduplicate_files(source_dir, target_dir)
