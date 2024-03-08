from ultralytics import YOLO
model = YOLO('yolov8n.pt')  # Load the pretrained model

source = 'path/to/image.jpg'  # Path to your image
results = model(source)

for box in results.boxes:
    cords = box.xyxy[0].tolist()  # Coordinates of the bounding box
    class_id = box.cls[0].item()  # Class ID of the detected object
    conf = box.conf[0].item()  # Confidence score
    print(f"Object type: {results.names[class_id]}")
    print(f"Coordinates: {cords}")
    print(f"Probability: {conf}")