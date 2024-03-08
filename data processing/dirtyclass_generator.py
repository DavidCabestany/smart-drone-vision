import os

# Define the path to the cleaned directory
CLEANED_DIR_PATH = r".\Genera_of_Pinopsida_raw"
# Define prefixes to exclude, ensuring all prefixes are lowercase for case-insensitive comparison
EXCLUDED_PREFIXES = ["animals_with_", "allée_des_sapins_"]


def is_excluded(dir_name):
    """
    Checks if a directory name starts with any of the excluded prefixes.

    Parameters:
    - dir_name (str): The directory name to check.

    Returns:
    - bool: True if the directory should be excluded, False otherwise.
    """
    return any(dir_name.startswith(prefix) for prefix in EXCLUDED_PREFIXES)


def extract_genus_name(dir_name):
    """
    Extracts the genus part of the directory name.

    Parameters:
    - dir_name (str): The directory name from which to extract the genus name.

    Returns:
    - str: The extracted genus name, capitalized.
    """
    return dir_name.split("_")[0].capitalize()


def collect_unique_classes(directory_path):
    """
    Walks through the directory structure to collect unique genus names, excluding specified prefixes.

    Parameters:
    - directory_path (str): The path to the directory to walk through.

    Returns:
    - set: A set of unique, capitalized genus names.
    """
    unique_classes = set()
    for root, dirs, _ in os.walk(directory_path):
        for dir_name in dirs:
            normalized_dir_name = dir_name.lower()  # Normalize the directory name
            if not is_excluded(normalized_dir_name):
                genus_name = extract_genus_name(normalized_dir_name)
                unique_classes.add(genus_name)
    return unique_classes


def write_classes_to_file(classes_set, file_path):
    """
    Writes each class name in the classes set to a file, sorted alphabetically.

    Parameters:
    - classes_set (set): A set containing class names to write.
    - file_path (str): The path to the file where class names should be written.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        for class_name in sorted(classes_set):
            file.write(f"{class_name}\n")
    print(f"Classes have been written to {os.path.abspath(file_path)}")


unique_classes = collect_unique_classes(CLEANED_DIR_PATH)
write_classes_to_file(unique_classes, "dirty_classes.txt")
