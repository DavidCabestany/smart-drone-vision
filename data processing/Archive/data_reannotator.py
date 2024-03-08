import os
import xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image

# Define the paths to your subset dataset and where to save the YOLO annotations
data_root = Path("/home/vjspycho/Desktop/gopro_app/split_imagenet")
annotations_root = data_root / "annotations"
images_root = data_root / "images"
yolo_annotations_root = data_root / "yolo_annotations"

# Create output directory for YOLO annotations
yolo_annotations_root.mkdir(parents=True, exist_ok=True)

# Create a mapping from ImageNet class IDs to integer labels
class_ids = sorted(os.listdir(annotations_root))
class_to_label = {class_id: i for i, class_id in enumerate(class_ids)}

# Convert the annotations to YOLO format
for class_id in class_ids:
    class_annotations_path = annotations_root / class_id
    class_images_path = images_root / class_id
    class_yolo_annotations_path = yolo_annotations_root / class_id
    class_yolo_annotations_path.mkdir(parents=True, exist_ok=True)

    for xml_file in os.listdir(class_annotations_path):
        xml_path = class_annotations_path / xml_file
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # Get image dimensions
        img_file = root.find('filename').text + ".JPEG"
        img_path = class_images_path / img_file
        img = Image.open(img_path)
        img_width, img_height = img.size
        
        # Create a YOLO annotation file
        yolo_annotation_path = class_yolo_annotations_path / (xml_file.replace('.xml', '.txt'))
        with open(yolo_annotation_path, 'w') as f:
            for obj in root.findall('object'):
                # Get class label
                label = class_to_label[class_id]
                
                # Get bounding box coordinates
                bndbox = obj.find('bndbox')
                xmin = int(bndbox.find('xmin').text)
                ymin = int(bndbox.find('ymin').text)
                xmax = int(bndbox.find('xmax').text)
                ymax = int(bndbox.find('ymax').text)
                
                # Convert coordinates to YOLO format
                x_center = ((xmin + xmax) / 2) / img_width
                y_center = ((ymin + ymax) / 2) / img_height
                width = (xmax - xmin) / img_width
                height = (ymax - ymin) / img_height
                
                # Write to YOLO annotation file
                f.write(f"{label} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

print("Annotation conversion completed.")
