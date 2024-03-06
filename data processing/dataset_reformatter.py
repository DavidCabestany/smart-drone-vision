import os
import shutil
import logging
from sklearn.model_selection import train_test_split
from typing import List

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_class_names(classes_file_path: str) -> List[str]:
    """
    Reads class names from a specified file.

    Parameters:
    - classes_file_path: Path to the classes.txt file.

    Returns:
    - List of class names.
    """
    try:
        with open(classes_file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        logging.warning(f"'classes.txt' not found in {classes_file_path}. Ensure class names are properly defined.")
        return []

def create_directories(base_path: str, folders: List[str]):
    """
    Creates directory structure for dataset preparation.

    Parameters:
    - base_path: The root path where directories will be created.
    - folders: A list of folder names to create.
    """
    for folder in folders:
        path = os.path.join(base_path, folder)
        os.makedirs(path, exist_ok=True)
        logging.info(f"Directory created: {path}")

def find_annotated_images(images_path: str, labels_path: str, image_format: str) -> List[str]:
    """
    Identifies images that have corresponding annotation files.

    Parameters:
    - images_path: Path to the images directory.
    - labels_path: Path to the labels directory.
    - image_format: The file extension of image files.

    Returns:
    - A list of base filenames for images with annotations.
    """
    annotated = [os.path.splitext(f)[0] for f in os.listdir(labels_path) if os.path.isfile(os.path.join(labels_path, f))]
    return [f for f in annotated if os.path.isfile(os.path.join(images_path, f + image_format))]

def copy_files(files: List[str], source_dir: str, destination_dir: str, file_type: str):
    """
    Copies specified files from source to destination directories, handling both images and labels.

    Parameters:
    - files: List of file base names to copy.
    - source_dir: Source directory path.
    - destination_dir: Destination directory path.
    - file_type: Type of file ('images' or 'labels') to handle the correct file extension.
    """
    ext = '.jpg' if file_type == 'images' else '.txt'
    for f in files:
        shutil.copy(os.path.join(source_dir, f + ext), os.path.join(destination_dir, f + ext))
        logging.info(f"File copied: {f + ext}")

def prepare_dataset(dataset_config: dict):
    """
    Prepares the dataset by organizing files into train and validation sets and writes a dataset configuration file.

    Parameters:
    - dataset_config: Configuration dictionary containing paths and settings.
    """
    class_names = read_class_names(dataset_config["classes_file_path"])
    if not class_names:
        return

    create_directories(dataset_config["dataset_path"], ['train/images', 'train/labels', 'val/images', 'val/labels'])

    annotated_images = find_annotated_images(dataset_config["images_path"], dataset_config["labels_path"], dataset_config["image_format"])
    train_images, val_images = train_test_split(annotated_images, test_size=0.2, random_state=42)

    copy_files(train_images, dataset_config["images_path"], os.path.join(dataset_config["dataset_path"], 'train', 'images'), 'images')
    copy_files(train_images, dataset_config["labels_path"], os.path.join(dataset_config["dataset_path"], 'train', 'labels'), 'labels')
    copy_files(val_images, dataset_config["images_path"], os.path.join(dataset_config["dataset_path"], 'val', 'images'), 'images')
    copy_files(val_images, dataset_config["labels_path"], os.path.join(dataset_config["dataset_path"], 'val', 'labels'), 'labels')

    # Generate and write dataset.yaml
    yaml_content = f"""
    path: {dataset_config["relative_path"]}
    train: train/images
    val: val/images

    nc: {len(class_names)}
    names: {class_names}
    """
    try:
        with open(os.path.join(dataset_config["dataset_path"], 'dataset.yaml'), 'w') as yaml_file:
            yaml_file.write(yaml_content.strip())
        logging.info("Dataset.yaml created successfully.")
    except Exception as e:
        logging.error(f"Error writing 'dataset.yaml': {e}")

def main():
    setup_logging()
    project_root = r'./Dataset/dataset'
    dataset_config = {
        "images_path": os.path.join(project_root, 'images'),
        "labels_path": os.path.join(project_root, 'labels'),
        "dataset_path": os.path.join(project_root, 'prepared_dataset'),
        "classes_file_path": os.path.join(project_root, 'labels', 'classes.txt'),
        "image_format": ".jpg",
        "relative_path": "../prepared_dataset"
    }
    prepare_dataset(dataset_config)

if __name__ == "__main__":
    main()
