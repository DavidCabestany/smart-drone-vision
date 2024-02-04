import torch
import cv2
import numpy as np

# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5l', pretrained=True)

# Function to process each frame from the video
def process_frame(frame):
    # Inference
    results = model(frame)

    # Extract data
    labels, cords = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]

    n = len(labels)
    if n:
        for i in range(n):
            row = cords[i]
            # If you have normalized cords, you can rescale them back
            x1, y1, x2, y2 = int(row[0]*frame.shape[1]), int(row[1]*frame.shape[0]), \
                             int(row[2]*frame.shape[1]), int(row[3]*frame.shape[0])
            conf = row[4]
            label = model.names[int(labels[i])]
            color = (0, 255, 0)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, f'{label} {conf:.2f}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    return frame

rtsp_url = 'your_rtsp_link_here'

# Load video stream from RTSP
cap = cv2.VideoCapture(rtsp_url)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame from BGR to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Process the frame for object detection
    processed_frame = process_frame(frame_rgb)
    # Convert back to BGR for OpenCV
    processed_frame_bgr = cv2.cvtColor(processed_frame, cv2.COLOR_RGB2BGR)

    cv2.imshow("Frame", processed_frame_bgr)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
