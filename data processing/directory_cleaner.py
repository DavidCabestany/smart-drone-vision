import os
import shutil
import re
import urllib.parse

# Define the path to the dataset directory
dataset_path = r".\Genera_of_Pinopsida_raw"
keywords = ["illustration", "illustrations", "historical", "trunk", "trunks", "fossil", "dead", "map"]
def should_delete_dir(dir_name):
    keywords = ["illustration", "illustrations", "historical", "trunk", "trunks", "fossil", "dead", "map", "bonsai"]
    if any(keyword in dir_name.lower() for keyword in keywords):
        return True
    # Special handling for "art" to avoid false positives
    if "art" in dir_name.lower() and not any(part for part in dir_name.lower().split('_') if "art" in part and len(part) > 3):
        return True
    return False

def normalize_dir_name(dir_name):
    # Decode URL-encoded characters and replace any sequence of symbols with a single underscore
    dir_name = urllib.parse.unquote(dir_name)
    return re.sub(r'[_\W]+', '_', dir_name)

def merge_directories(src, dest):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dest, item)
        if os.path.isdir(s):
            if not os.path.exists(d):
                os.makedirs(d)
            merge_directories(s, d)  # Recursively merge directories
            os.rmdir(s)  # Remove the source directory after its content has been moved
        else:
            if not os.path.exists(d):
                shutil.move(s, d)
            else:
                os.remove(s)  # Remove the source file if the destination file exists

def rename_files_in_directory(dir_path, base_name):
    files = sorted([f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))])
    
    for i, file_name in enumerate(files, 1):
        file_extension = os.path.splitext(file_name)[1]
        if file_extension.lower() in ['.jpg', '.jpeg', '.png']:
            new_file_name = f"{base_name}_{i:04d}{file_extension}"
            new_file_path = os.path.join(dir_path, new_file_name)
            if not os.path.exists(new_file_path):
                os.rename(os.path.join(dir_path, file_name), new_file_path)
                print(f"Renamed '{file_name}' to '{new_file_name}'")
            else:
                print(f"Skipped renaming of '{file_name}' to '{new_file_name}' as it already exists")

def delete_files_with_keywords(dir_path, keywords):
    # New function to delete files based on keywords
    for root, dirs, files in os.walk(dir_path, topdown=False):
        for name in files:
            if any(keyword in name.lower() for keyword in keywords):
                os.remove(os.path.join(root, name))
                print(f"Deleted file '{name}' due to matching exclusion criteria")

def clean_and_merge_directories(dir_path):
    dirs = next(os.walk(dir_path))[1]

    for dir_name in dirs:
        normalized_name = normalize_dir_name(dir_name)
        if should_delete_dir(normalized_name):
            shutil.rmtree(os.path.join(dir_path, dir_name))
            print(f"Deleted '{dir_name}' due to matching exclusion criteria")
            continue

        clean_name = normalized_name.strip('_')
        clean_name = re.sub(r'\s+', '_', clean_name)

        if clean_name.startswith("Unidentified_"):
            genus_name = clean_name[13:]  # Remove "Unidentified_" prefix
        else:
            genus_name = clean_name

        current_dir = os.path.join(dir_path, dir_name)
        new_dir = os.path.join(dir_path, genus_name)

        if not os.path.exists(new_dir):
            os.rename(current_dir, new_dir)
            print(f"Renamed '{dir_name}' to '{genus_name}'")
        else:
            # Case-insensitive comparison for directory paths
            if current_dir.lower() != new_dir.lower():
                print(f"Merging '{dir_name}' into '{genus_name}'")
                merge_directories(current_dir, new_dir)
                # Check if directory is empty before removing
                if not os.listdir(current_dir):
                    os.rmdir(current_dir)

        # Call the new function to delete files with keywords
        delete_files_with_keywords(new_dir, keywords)
        rename_files_in_directory(new_dir, genus_name)

# Run the clean and merge process
clean_and_merge_directories(dataset_path)
