import os
import shutil
import random
import re

def prepare_images_for_annotation(source_dir: str, test_dir: str, images_to_keep: int = 6) -> None:
    """
    Prepares images for annotation by moving images with special characters and excess images to a test directory.

    Args:
    source_dir (str): Directory containing source images.
    test_dir (str): Directory where images with special characters or excess images will be moved.
    images_to_keep (int): Number of images to keep in each category within the source directory.
    """
    # Ensure the test directory exists
    os.makedirs(test_dir, exist_ok=True)

    def contains_special_characters(filename: str) -> bool:
        """Checks if the filename contains special characters."""
        return not re.match(r'^[\w\-]+\.[\w\-]+$', filename)

    def move_images_with_special_chars() -> None:
        """Moves images with special characters to the test directory."""
        for image in os.listdir(source_dir):
            if contains_special_characters(image):
                shutil.move(os.path.join(source_dir, image), os.path.join(test_dir, image))

    def select_and_move_images() -> None:
        """Selects and moves excess images to the test directory."""
        folder_images = {}
        for image in os.listdir(source_dir):
            original_folder_name = "_".join(image.split('_')[:-1])
            folder_images.setdefault(original_folder_name, []).append(image)

        for images in folder_images.values():
            if len(images) > images_to_keep:
                images_to_move = set(images) - set(random.sample(images, images_to_keep))
                for image in images_to_move:
                    shutil.move(os.path.join(source_dir, image), os.path.join(test_dir, image))

    move_images_with_special_chars()
    select_and_move_images()

def clean_up_after_annotation(source_dir: str, annotation_dir: str, test_dir: str) -> None:
    """
    Cleans up after annotation by moving images without corresponding annotation files to a test directory.

    Args:
    source_dir (str): Directory containing source images.
    annotation_dir (str): Directory containing annotation files.
    test_dir (str): Directory where images without corresponding annotation files will be moved.
    """
    # Ensure the test directory exists
    os.makedirs(test_dir, exist_ok=True)

    for image_file in os.listdir(source_dir):
        annotation_file = os.path.splitext(image_file)[0] + '.txt'
        if not os.path.exists(os.path.join(annotation_dir, annotation_file)):
            shutil.move(os.path.join(source_dir, image_file), os.path.join(test_dir, image_file))

# Example usage

# To prepare images for annotation
source_dir = r'.\Dataset\Pinopsida\images'
test_dir = r'.\Dataset\Pinopsida\test'
# prepare_images_for_annotation(source_dir, test_dir)

# To clean up after annotation
annotation_dir = r'.\Dataset\Pinopsida\labels'
clean_up_after_annotation(source_dir, annotation_dir, test_dir)
