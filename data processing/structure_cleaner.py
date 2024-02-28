import os
import shutil
import re
import urllib.parse

# Define the path to the dataset directory
dataset_path = "C:/Users/David/Projects/smart-drone-vision/Dataset/Larix"

def merge_directories(src, dest):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dest, item)
        if os.path.isdir(s):
            shutil.move(s, dest)
        else:
            if not os.path.exists(d):
                shutil.move(s, dest)
            else:
                os.unlink(s)  # Remove the file if it exists in the destination

def rename_files_in_directory(dir_path, base_name):
    # List all files in directory and sort them to maintain a consistent order
    files = sorted([f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))])
    
    # Rename files to match directory name with a sequential number
    for i, file_name in enumerate(files, 1):
        file_extension = os.path.splitext(file_name)[1]
        if file_extension.lower() in ['.jpg', '.jpeg', '.png']:  # Add any other file types if necessary
            new_file_name = f"{base_name}_{i:04d}{file_extension}"
            os.rename(os.path.join(dir_path, file_name), os.path.join(dir_path, new_file_name))
            print(f"Renamed '{file_name}' to '{new_file_name}'")

def clean_and_merge_directories(dir_path):
    dirs = next(os.walk(dir_path))[1]
    cleaned_dir_names = {}

    for dir_name in dirs:
        # Decode the URL encoded strings and clean up the directory name
        clean_name = urllib.parse.unquote(dir_name)
        clean_name = re.sub(r'[^\w\s-]', '_', clean_name)
        clean_name = re.sub(r'\s+', '_', clean_name)
        # Keep only the genus part of the name (assuming it is the first part of the directory name)
        genus_name = clean_name.split('_')[0] + '_' + clean_name.split('_')[1]

        # Full paths for current and new directories
        current_dir = os.path.join(dir_path, dir_name)
        new_dir = os.path.join(dir_path, genus_name)

        # If this is the first time we see this genus, rename the directory
        if genus_name not in cleaned_dir_names:
            os.rename(current_dir, new_dir)
            cleaned_dir_names[genus_name] = new_dir
            print(f"Renamed '{current_dir}' to '{new_dir}'")
        else:
            # If the genus directory already exists, move the contents
            print(f"Merging '{current_dir}' into '{new_dir}'")
            merge_directories(current_dir, cleaned_dir_names[genus_name])
            os.rmdir(current_dir)  # Remove the now-empty source directory

        # Rename the files in the directory
        rename_files_in_directory(new_dir, genus_name)

# Run the clean, merge, and rename process
clean_and_merge_directories(dataset_path)

