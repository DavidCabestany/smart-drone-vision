import os
import shutil

# Define the source and target directories
source_dir = r"C:\Users\David\Projects\smart-drone-vision\downloaded_Genera_of_Pinopsida"

target_dir = r'C:\Users\David\Projects\smart-drone-vision\Dataset\Pinopsida\images'

# Check if target directory exists, create if not
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

# Walk through all files in subdirectories of the source
for subdir, _, files in os.walk(source_dir):
    for file in files:
        # Construct the full file path
        file_path = os.path.join(subdir, file)
        # Move each file to the target directory
        shutil.move(file_path, target_dir)

print("All images have been moved to the target directory.")
