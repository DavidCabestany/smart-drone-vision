import os
import shutil
from sklearn.model_selection import train_test_split

# Define paths
images_path = r'C:\Users\David\Projects\smart-drone-vision\Dataset\Pinopsida\images'
labels_path = r'C:\Users\David\Projects\smart-drone-vision\Dataset\Pinopsida\labels'
dataset_path = r'C:\Users\David\Projects\smart-drone-vision\Dataset\Pinopsida\dataset'
classes_file_path = os.path.join(labels_path, 'classes.txt')

# Image format
image_format = '.jpg'  # Adjust as needed

# Read class names from the classes.txt file
class_names = []
if os.path.exists(classes_file_path):
    with open(classes_file_path, 'r') as file:
        class_names = [line.strip() for line in file.readlines()]
else:
    print(f"Warning: 'classes.txt' not found in {classes_file_path}. Ensure class names are properly defined.")

# Create new directories
for folder in ['train', 'val']:
    for sub_folder in ['images', 'labels']:
        os.makedirs(os.path.join(dataset_path, sub_folder, folder), exist_ok=True)

# Get all images that have corresponding annotation files
annotated_images = [os.path.splitext(f)[0] for f in os.listdir(labels_path) if os.path.isfile(os.path.join(labels_path, f))]
annotated_images = [f for f in annotated_images if os.path.isfile(os.path.join(images_path, f + image_format))]

# Split data into train and validation sets
train_images, val_images = train_test_split(annotated_images, test_size=0.2, random_state=42)

# Function to copy files to new structure
def copy_files(files, source_images, source_labels, dest_images, dest_labels):
    for f in files:
        shutil.copy(os.path.join(source_images, f + image_format), os.path.join(dest_images, f + image_format))
        shutil.copy(os.path.join(source_labels, f + '.txt'), os.path.join(dest_labels, f + '.txt'))

# Copy training and validation files
copy_files(train_images, images_path, labels_path, os.path.join(dataset_path, 'images', 'train'), os.path.join(dataset_path, 'labels', 'train'))
copy_files(val_images, images_path, labels_path, os.path.join(dataset_path, 'images', 'val'), os.path.join(dataset_path, 'labels', 'val'))

# Correct nc based on actual class count
nc = len(class_names)

# Generate dataset.yaml content correctly
yaml_content = f"""
path: {dataset_path.replace('\\', '/')}
train: images/train
val: images/val

nc: {nc}
names: {class_names}
"""

# Write the dataset.yaml file
yaml_path = os.path.join(dataset_path, 'dataset.yaml')
try:
    with open(yaml_path, 'w') as yaml_file:
        yaml_file.write(yaml_content.strip())
    print("Dataset successfully restructured for YOLO training, and dataset.yaml created.")
except Exception as e:
    print(f"Error writing 'dataset.yaml': {e}")
