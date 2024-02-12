import torch
import cv2
import numpy as np
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the YOLOv5 model
try:
    model = torch.hub.load('ultralytics/yolov5', 'yolov5l', pretrained=True)
    logging.info("YOLOv5 model loaded successfully.")
except Exception as e:
    logging.error(f"Failed to load model: {e}")
    exit()

def process_frame(frame):
    try:
        results = model(frame)
        labels, cords = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
        n = len(labels)
        if n:
            for i in range(n):
                row = cords[i]
                x1, y1, x2, y2 = int(row[0]*frame.shape[1]), int(row[1]*frame.shape[0]), \
                                 int(row[2]*frame.shape[1]), int(row[3]*frame.shape[0])
                conf = row[4]
                label = model.names[int(labels[i])]
                color = (0, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f'{label} {conf:.2f}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
    except Exception as e:
        logging.error(f"Error processing frame: {e}")
    return frame

# RTSP URL
rtsp_url = 'rtmp://192.168.10.152/live'

try:
    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        logging.error("Failed to open video stream.")
        exit()
    logging.info("Video stream opened successfully.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            logging.info("No frame retrieved from the stream.")
            break

        # Process the frame for object detection and display
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        processed_frame = process_frame(frame_rgb)
        processed_frame_bgr = cv2.cvtColor(processed_frame, cv2.COLOR_RGB2BGR)
        cv2.imshow("Frame", processed_frame_bgr)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    logging.info("Script interrupted by user.")
finally:
    cap.release()
    cv2.destroyAllWindows()
    logging.info("Resources released and script terminated.")

