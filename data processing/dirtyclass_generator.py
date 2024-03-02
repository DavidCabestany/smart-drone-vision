import os

# Define the path to the cleaned directory
cleaned_dir_path = r"C:\Users\David\Projects\smart-drone-vision\Genera_of_Pinopsida_raw"

# Define prefixes to exclude
excluded_prefixes = ["animals_with_", "Allée_des_Sapins_",]

# Set to store unique class names
unique_classes = set()

# Function to check if the directory name starts with any of the excluded prefixes
def is_excluded(dir_name):
    return any(dir_name.startswith(prefix) for prefix in excluded_prefixes)

# Walk through the directory structure
for root, dirs, files in os.walk(cleaned_dir_path):
    for dir_name in dirs:
        # Normalize the directory name by converting it to lowercase
        normalized_dir_name = dir_name.lower()
        # Extract the genus part of the directory name
        genus_name = normalized_dir_name.split('_')[0]
        # Check if the directory should be excluded based on its prefix
        if not is_excluded(normalized_dir_name):
            unique_classes.add(genus_name.capitalize())

# Write the unique class names to a text file
with open("dirty_classes.txt", "w", encoding="utf-8") as file:
    for class_name in sorted(unique_classes):
        file.write(f"{class_name}\n")

print(f"Classes have been written to {os.path.abspath('dirty_classes.txt')}")
