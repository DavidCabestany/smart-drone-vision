import os
import sys
import time
import cv2
import torch
from pathlib import Path

def is_valid_image(file_path):
    """
    Check if the file is a valid image by attempting to open it with OpenCV.

    Parameters:
    - file_path: The path to the image file.

    Returns:
    - bool: True if the file is a valid image, False otherwise.
    """
    try:
        img = cv2.imread(str(file_path), cv2.IMREAD_UNCHANGED)
        if img is not None:
            return True
        else:
            return False
    except Exception as e:
        print(f"Invalid image {file_path}: {e}")
        return False


# Set the path to the directory where the images are saved
images_dir = Path(r"C:\Users\David\Projects\smart-drone-vision\Dataset\test")

# Set the path to the directory where the detected images will be saved
output_dir = Path(r"C:\Users\David\Projects\smart-drone-vision\detected_images")
output_dir.mkdir(parents=True, exist_ok=True)

# Path to your fine-tuned model weights
weights_path = r"C:\Users\David\Projects\smart-drone-vision\yolov5\runs\train\exp5\weights\best.pt"

# Load the fine-tuned YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path=weights_path, force_reload=True)

# Optionally adjust model parameters
model.conf = 0.45  # confidence threshold (0-1)
model.iou = 0.45   # NMS IoU threshold (0-1)

# Define the custom progress bar function
def custom_progress_bar(current, total, bar_length=50):
    fraction = current / total
    arrow = int(fraction * bar_length - 1) * '-' + 'DRONE2MAX'
    padding = (bar_length - len(arrow)) * ' '
    ending = '\n' if current == total else '\r'
    return f'[{arrow}{padding}] {current}/{total}{ending}'

# Get the list of image paths and the total number of images
image_paths = list(images_dir.glob('*.jpg')) + list(images_dir.glob('*.png'))
total_images = len(image_paths)

# Process each image in the directory
for i, img_path in enumerate(image_paths):
    if not is_valid_image(img_path):
        continue
    # Print custom progress bar
    sys.stdout.write(custom_progress_bar(i + 1, total_images))
    sys.stdout.flush()
    
    # Read the image
    img = cv2.imread(str(img_path))
    
    # Inference
    results = model(img, size=640)
    
    # Render results on the image
    img_detected = results.render()[0]
    img_detected = cv2.cvtColor(img_detected, cv2.COLOR_BGR2RGB)
    
    # Save the image
    output_path = output_dir / img_path.name
    cv2.imwrite(str(output_path), img_detected)

    # Simulate processing time
    time.sleep(0.1)  # Remove this in real usage

# Ensure the final progress shows 100%
sys.stdout.write(custom_progress_bar(total_images, total_images))
sys.stdout.write('\n')
sys.stdout.flush()

print("Processing complete. Detected images are saved in:", output_dir)
