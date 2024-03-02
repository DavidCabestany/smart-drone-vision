import os
import shutil
import hashlib

# Define the source and target directories
source_dir = r"C:\Users\David\Projects\smart-drone-vision\Genera_of_Pinopsida_raw"
target_dir = r'C:\Users\David\Projects\smart-drone-vision\Dataset\Pinopsida\images2'

# Ensure the target directory exists
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

def file_hash(file_path):
    """Generate a hash for a file's contents."""
    hash_obj = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

def is_file_different(source_file, target_file):
    """Check if the content of two files is different based on their hash."""
    return file_hash(source_file) != file_hash(target_file)

# Function to generate a new file name if a file already exists
def get_new_file_name(target_dir, file_name):
    base_name, extension = os.path.splitext(file_name)
    counter = 1
    new_file_name = file_name
    while os.path.exists(os.path.join(target_dir, new_file_name)):
        new_file_name = f"{base_name}_({counter}){extension}"
        counter += 1
    return new_file_name

# Walk through all files in subdirectories of the source
for subdir, _, files in os.walk(source_dir):
    for file in files:
        source_file_path = os.path.join(subdir, file)
        target_file_path = os.path.join(target_dir, file)
        
        # Check if the file already exists in the target directory
        if os.path.exists(target_file_path):
            # Decide to move or not based on file content
            if is_file_different(source_file_path, target_file_path):
                # Files are different; get a new name for the source file
                new_file_name = get_new_file_name(target_dir, file)
                target_file_path = os.path.join(target_dir, new_file_name)
            else:
                # Files are the same; skip moving this file
                print(f"Skipped '{file}' as it already exists with the same content in the target directory.")
                continue
        
        # Move the file
        shutil.move(source_file_path, target_file_path)

print("All images have been moved or skipped if identical to the target directory.")
