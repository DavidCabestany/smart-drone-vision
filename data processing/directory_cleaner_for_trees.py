import os
import shutil
import re
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

DATASET_PATH = os.getenv("DATASET_PATH", "your/path/to/dataset")


keywords_str = os.getenv("KEYWORDS", "your,keywords,here")
KEYWORDS = [keyword.strip() for keyword in keywords_str.split(",")]

exclusions_str = os.getenv("EXCLUDED_PREFIXES", "your,list,of,exclusions")
EXCLUDED_PREFIXES = [exclusion.strip() for exclusion in exclusions_str.split(",")]

extensions_str = os.getenv("SUPPORTED_EXTENSIONS", ".jpg,.jpeg,.png")
SUPPORTED_EXTENSIONS = [ext.strip() for ext in extensions_str.split(",")]


def should_delete_dir(dir_name, keywords):
    """
    Determines if a directory should be deleted based on matching keywords.

    Parameters:
    - dir_name (str): The name of the directory to check.
    - keywords (list): A list of keywords to match against the directory name.

    Returns:
    - bool: True if the directory matches any keyword; otherwise, False.
    """
    return any(keyword in dir_name.lower() for keyword in keywords)


def normalize_dir_name(dir_name):
    """
    Normalizes directory names by decoding URL-encoded strings and replacing non-word characters with underscores.

    Parameters:
    - dir_name (str): The directory name to normalize.

    Returns:
    - str: The normalized directory name.
    """
    return re.sub(r"[_\W]+", "_", urllib.parse.unquote(dir_name))


def merge_directories(src, dest):
    """
    Recursively merges the contents of the source directory into the destination directory.

    Parameters:
    - src (str): The path of the source directory.
    - dest (str): The path of the destination directory.
    """
    for item in os.listdir(src):
        s_path, d_path = os.path.join(src, item), os.path.join(dest, item)
        if os.path.isdir(s_path):
            if not os.path.exists(d_path):
                os.makedirs(d_path)
            merge_directories(s_path, d_path)
            os.rmdir(s_path)
        elif not os.path.exists(d_path):
            shutil.move(s_path, d_path)
        else:
            os.remove(s_path)


def rename_files_in_directory(dir_path, base_name):
    """
    Renames all supported files in a directory to a uniform naming convention based on a base name.

    Parameters:
    - dir_path (str): The path of the directory containing the files to rename.
    - base_name (str): The base name to use for renaming files.
    """
    for i, file_name in enumerate(sorted(os.listdir(dir_path)), 1):
        full_path = os.path.join(dir_path, file_name)
        if os.path.isfile(full_path):
            file_extension = os.path.splitext(file_name)[1].lower()
            if file_extension in SUPPORTED_EXTENSIONS:
                new_name = f"{base_name}_{i:04d}{file_extension}"
                new_path = os.path.join(dir_path, new_name)
                if not os.path.exists(new_path):
                    os.rename(full_path, new_path)
                    print(f"Renamed '{file_name}' to '{new_name}'")
                else:
                    print(
                        f"Skipped renaming '{file_name}' to '{new_name}' as it already exists"
                    )


def clean_and_merge_directories(dir_path):
    """
    Cleans and merges directories in a dataset by deleting directories matching specific keywords, normalizing directory names,
    and merging directories when applicable.

    Parameters:
    - dir_path (str): The root path of the dataset directory to clean and merge.
    """
    dirs = next(os.walk(dir_path))[1]

    for dir_name in dirs:
        normalized_name = normalize_dir_name(dir_name)
        if should_delete_dir(normalized_name, KEYWORDS):
            shutil.rmtree(os.path.join(dir_path, dir_name))
            print(f"Deleted '{dir_name}' due to matching exclusion criteria")
            continue

        # Handle excluded prefixes and capitalize the genus name
        prefix_length = next(
            (
                len(prefix)
                for prefix in EXCLUDED_PREFIXES
                if normalized_name.startswith(prefix)
            ),
            0,
        )
        genus_name = normalized_name[prefix_length:].capitalize()
        target_dir, current_dir = os.path.join(dir_path, genus_name), os.path.join(
            dir_path, dir_name
        )

        if not os.path.exists(target_dir):
            os.rename(current_dir, target_dir)
            print(f"Renamed '{dir_name}' to '{genus_name}'")
        elif current_dir.lower() != target_dir.lower():
            merge_directories(current_dir, target_dir)
            if not os.listdir(current_dir):
                os.rmdir(current_dir)


# Execute the cleaning and merging process
clean_and_merge_directories(DATASET_PATH)
