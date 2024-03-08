import filecmp
import os


def summarize_differences(dir1, dir2):
    """
    Compares two directories and prints a summary of differences including files that are missing in either directory,
    and files that are present in both but differ.

    Parameters:
    - dir1 (str): Path to the first directory to compare.
    - dir2 (str): Path to the second directory to compare.

    The function prints:
    - The path where differences were found.
    - Files missing in dir1.
    - Files missing in dir2.
    - Files that differ between dir1 and dir2.
    """
    dcmp = filecmp.dircmp(dir1, dir2)

    def compare(dcmp, path_prefix=""):
        """
        Recursively compares directories reported by filecmp.dircmp and prints differences.

        Parameters:
        - dcmp (filecmp.dircmp): A directory comparison object.
        - path_prefix (str): A prefix for the path to indicate the current directory's relative path from the initial directories being compared.
        """
        differences = {
            "path": path_prefix,
            "missing_in_dir1": dcmp.right_only,
            "missing_in_dir2": dcmp.left_only,
            "different_files": dcmp.diff_files,
        }
        if (
            differences["missing_in_dir1"]
            or differences["missing_in_dir2"]
            or differences["different_files"]
        ):
            print_differences(differences)

        for subdir in dcmp.common_dirs:
            sub_dcmp = filecmp.dircmp(
                os.path.join(dcmp.left, subdir), os.path.join(dcmp.right, subdir)
            )
            compare(sub_dcmp, os.path.join(path_prefix, subdir))

    def print_differences(differences):
        """
        Prints the differences between two directories based on the data provided by compare().

        Parameters:
        - differences (dict): A dictionary containing the path, files missing in dir1, missing in dir2, and different files.
        """
        if (
            differences["missing_in_dir1"]
            or differences["missing_in_dir2"]
            or differences["different_files"]
        ):
            print(f'Path: {differences["path"]}')
            if differences["missing_in_dir1"]:
                print(
                    f'Missing in {os.path.basename(dir1)}: {differences["missing_in_dir1"]}'
                )
            if differences["missing_in_dir2"]:
                print(
                    f'Missing in {os.path.basename(dir2)}: {differences["missing_in_dir2"]}'
                )
            if differences["different_files"]:
                print(f'Different files: {differences["different_files"]}')
            print()

    compare(dcmp)


dir1 = r".\downloaded_Genera_of_Pinopsida"
dir2 = r".\downloaded_Genera_of_Pinopsida_2"

summarize_differences(dir1, dir2)
