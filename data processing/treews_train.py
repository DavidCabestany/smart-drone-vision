import os
import shutil
from sklearn.model_selection import train_test_split

# Define paths
images_path = 'C:\\Users\\David\\Projects\\smart-drone-vision\\Dataset\\Larix annotation\\images'  # Path where all images are stored
labels_path = 'C:\\Users\\David\\Projects\\smart-drone-vision\\Dataset\\Larix annotation\\labels'  # Path where all corresponding .txt files are stored
dataset_path = 'C:\\Users\\David\\Projects\\smart-drone-vision\\Dataset\\Larix annotation\\dataset'  # Path where the new dataset structure will be created

# Create new directories
os.makedirs(os.path.join(dataset_path, 'images', 'train'), exist_ok=True)
os.makedirs(os.path.join(dataset_path, 'images', 'val'), exist_ok=True)
os.makedirs(os.path.join(dataset_path, 'labels', 'train'), exist_ok=True)
os.makedirs(os.path.join(dataset_path, 'labels', 'val'), exist_ok=True)

# Get all images that have corresponding annotation files
annotated_images = [os.path.splitext(f)[0] for f in os.listdir(labels_path) if os.path.isfile(os.path.join(labels_path, f))]
annotated_images = [f for f in annotated_images if os.path.isfile(os.path.join(images_path, f + '.jpg'))]  # Change '.jpg' if using a different image format

# Split data into train and validation sets
train_images, val_images = train_test_split(annotated_images, test_size=0.2, random_state=42)  # Change test_size as needed

# Function to copy files to new structure
def copy_files(files, source_images, source_labels, dest_images, dest_labels):
    for f in files:
        image_name = f + '.jpg'  # Change '.jpg' if using a different image format
        label_name = f + '.txt'
        
        # Copy image
        shutil.copy(os.path.join(source_images, image_name), os.path.join(dest_images, image_name))
        # Copy label
        shutil.copy(os.path.join(source_labels, label_name), os.path.join(dest_labels, label_name))

# Copy training files
copy_files(train_images, images_path, labels_path, os.path.join(dataset_path, 'images', 'train'), os.path.join(dataset_path, 'labels', 'train'))

# Copy validation files
copy_files(val_images, images_path, labels_path, os.path.join(dataset_path, 'images', 'val'), os.path.join(dataset_path, 'labels', 'val'))

print("Dataset successfully restructured for YOLO training.")
