import os
import random
import shutil
from pathlib import Path

# Define the paths to your ImageNet dataset
data_root = Path("/home/vjspycho/Desktop/gopro_app/ImageNet/")
annotations_root = data_root / "ILSVRC/Annotations/CLS-LOC/train"
images_root = data_root / "ILSVRC/Data/CLS-LOC/train"

# Define the output paths where the subset of the data will be saved
output_annotations_root = Path("/home/vjspycho/Desktop/gopro_app/split_imagenet/annotations")
output_images_root = Path("/home/vjspycho/Desktop/gopro_app/split_imagenet/images")

# Get the list of all class directories
all_classes = sorted(os.listdir(annotations_root))

# Randomly select 20% of the classes
selected_classes = random.sample(all_classes, len(all_classes) // 5)

# Create output directories if they don't exist
output_annotations_root.mkdir(parents=True, exist_ok=True)
output_images_root.mkdir(parents=True, exist_ok=True)

# Copy the selected classes' annotations and images to the output directories
for cls in selected_classes:
    shutil.copytree(annotations_root / cls, output_annotations_root / cls)
    shutil.copytree(images_root / cls, output_images_root / cls)

print(f"Copied {len(selected_classes)} classes to the output directories")
