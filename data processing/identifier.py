import os
from pathlib import Path
from PIL import Image
import random
import matplotlib.pyplot as plt

# Define the paths to your images and annotations directories
images_dir = Path("/home/vjspycho/Desktop/gopro_app/split_imagenet/annotations")
annotations_dir = Path("/home/vjspycho/Desktop/gopro_app/split_imagenet/yolo_annotations")


# Create a mapping from old class IDs to new class names
id_to_name = {}
for i, class_dir in enumerate(sorted(images_dir.iterdir())):
    if class_dir.is_dir():
        # Randomly select a few images to show
        sample_images = random.sample(list(class_dir.glob("*.JPEG")), min(3, len(list(class_dir.glob("*.JPEG")))))
        
        for image_file in sample_images:
            # Open the image using PIL
            image = Image.open(image_file)
            
            # Display the image using matplotlib
            plt.imshow(image)
            plt.axis('off')  # No axes for this plot
            plt.show()
        
        # Ask the user to identify the class based on the shown images
        class_name = input(f"Please identify the class represented by the images from directory '{class_dir.name}': ")
        id_to_name[str(i)] = class_name

# Update the class IDs in the YOLO annotation files
for class_id, class_name in id_to_name.items():
    class_annotations_dir = annotations_dir / class_id
    if class_annotations_dir.exists():
        for annotation_file in class_annotations_dir.iterdir():
            if annotation_file.suffix == '.txt':
                with open(annotation_file, 'r') as file:
                    lines = file.readlines()
                
                # Update the class ID in each line with the new class name
                updated_lines = [f"{class_name} " + line.split(' ', 1)[1] for line in lines]
                
                # Write the updated lines back to the file
                with open(annotation_file, 'w') as file:
                    file.writelines(updated_lines)

print("Updated class IDs in YOLO annotation files.")
