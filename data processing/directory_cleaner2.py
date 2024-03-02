import os
import shutil
import re
import urllib.parse

# Define the path to the dataset directory
dataset_path = r"C:\Users\David\Projects\smart-drone-vision\Genera_of_Pinopsida_raw"
keywords = [
    "illustration",
    "illustrations",
    "historical",
    "trunk",
    "trunks",
    "fossil",
    "dead",
    "map",
    "bonsai",
    "Allée",
]

excluded_prefixes = ["Unidentified_", "Allée"]


def should_delete_dir(dir_name, keywords):
    dir_name_lower = dir_name.lower()
    if any(keyword in dir_name_lower for keyword in keywords):
        return True
    return False


def normalize_dir_name(dir_name):
    dir_name = urllib.parse.unquote(dir_name)
    return re.sub(r"[_\W]+", "_", dir_name)


def merge_directories(src, dest):
    for item in os.listdir(src):
        s_path = os.path.join(src, item)
        d_path = os.path.join(dest, item)
        if os.path.isdir(s_path):
            if not os.path.exists(d_path):
                os.makedirs(d_path)
            merge_directories(s_path, d_path)
            os.rmdir(s_path)
        else:
            if not os.path.exists(d_path):
                shutil.move(s_path, d_path)
            else:
                os.remove(s_path)


def rename_files_in_directory(dir_path, base_name):
    for i, file_name in enumerate(sorted(os.listdir(dir_path)), 1):
        full_path = os.path.join(dir_path, file_name)
        if os.path.isfile(full_path):
            file_extension = os.path.splitext(file_name)[1].lower()
            if file_extension in [".jpg", ".jpeg", ".png"]:
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
    dirs = next(os.walk(dir_path))[1]

    for dir_name in dirs:
        normalized_name = normalize_dir_name(dir_name)
        if should_delete_dir(normalized_name, keywords):
            shutil.rmtree(os.path.join(dir_path, dir_name))
            print(f"Deleted '{dir_name}' due to matching exclusion criteria")
            continue

        # Handling prefixes like "Unidentified" and "Allée"
        prefix_length = next(
            (
                len(prefix)
                for prefix in excluded_prefixes
                if normalized_name.startswith(prefix)
            ),
            0,
        )
        genus_name = normalized_name[prefix_length:].capitalize()

        target_dir = os.path.join(dir_path, genus_name)
        current_dir = os.path.join(dir_path, dir_name)

        if not os.path.exists(target_dir):
            os.rename(current_dir, target_dir)
            print(f"Renamed '{dir_name}' to '{genus_name}'")
        else:
            if current_dir.lower() != target_dir.lower():
                merge_directories(current_dir, target_dir)
                if not os.listdir(current_dir):
                    os.rmdir(current_dir)


clean_and_merge_directories(dataset_path)
