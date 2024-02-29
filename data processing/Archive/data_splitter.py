import os
import random
import shutil
from pathlib import Path

# Define paths to the ImageNet dataset
data_root = Path("/home/vjspycho/Desktop/gopro_app/ImageNet/")
annotations_root = data_root / "ILSVRC/Annotations/CLS-LOC/train"
images_root = data_root / "ILSVRC/Data/CLS-LOC/train"

# Define output paths for the data subset
output_annotations_root = Path("/home/vjspycho/Desktop/gopro_app/split_imagenet/annotations")
output_images_root = Path("/home/vjspycho/Desktop/gopro_app/split_imagenet/images")

# Get a sorted list of all class directories
all_classes = sorted(os.listdir(str(annotations_root)))

# Randomly select 20% of the classes
selected_classes = random.sample(all_classes, k=len(all_classes) // 5)

# Ensure output directories exist
output_annotations_root.mkdir(parents=True, exist_ok=True)
output_images_root.mkdir(parents=True, exist_ok=True)

# Copy selected classes' annotations and images to output directories
for cls in selected_classes:
    shutil.copytree(src=annotations_root / cls, dst=output_annotations_root / cls)
    shutil.copytree(src=images_root / cls, dst=output_images_root / cls)

print(f"Copied {len(selected_classes)} classes to the output directories.")
