import filecmp
import os

def summarize_differences(dir1, dir2):
    dcmp = filecmp.dircmp(dir1, dir2)

    def compare(dcmp, path_prefix=""):
        differences = {
            "path": path_prefix,
            "missing_in_dir1": dcmp.right_only,
            "missing_in_dir2": dcmp.left_only,
            "different_files": dcmp.diff_files
        }
        if differences["missing_in_dir1"] or differences["missing_in_dir2"] or differences["different_files"]:
            print_differences(differences)

        for subdir in dcmp.common_dirs:
            sub_dcmp = filecmp.dircmp(os.path.join(dcmp.left, subdir), os.path.join(dcmp.right, subdir))
            compare(sub_dcmp, os.path.join(path_prefix, subdir))

    def print_differences(differences):
        if differences["missing_in_dir1"] or differences["missing_in_dir2"] or differences["different_files"]:
            print(f'Path: {differences["path"]}')
            if differences["missing_in_dir1"]:
                print(f'Missing in {os.path.basename(dir1)}: {differences["missing_in_dir1"]}')
            if differences["missing_in_dir2"]:
                print(f'Missing in {os.path.basename(dir2)}: {differences["missing_in_dir2"]}')
            if differences["different_files"]:
                print(f'Different files: {differences["different_files"]}')
            print()  # Add a newline for better readability

    compare(dcmp)
dir1 = r'C:\Users\David\Projects\smart-drone-vision\downloaded_Genera_of_Pinopsida'
dir2 = r'C:\Users\David\Projects\smart-drone-vision\downloaded_Genera_of_Pinopsida_2'

summarize_differences(dir1, dir2)
