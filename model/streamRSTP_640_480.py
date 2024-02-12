import torch
import cv2
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    model = torch.hub.load('ultralytics/yolov5', 'yolov5l', pretrained=True)
    logging.info("YOLOv5 model loaded successfully.")
except Exception as e:
    logging.error(f"Failed to load model: {e}")
    exit()

def process_frame(frame):
    # Resize frame for faster processing
    frame_resized = cv2.resize(frame, (640, 480))  # Resize to speed up processing
    frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
    
    results = model(frame_rgb)
    labels, cords = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
    n = len(labels)
    if n:
        for i in range(n):
            row = cords[i]
            x1, y1, x2, y2 = int(row[0]*frame_resized.shape[1]), int(row[1]*frame_resized.shape[0]), \
                             int(row[2]*frame_resized.shape[1]), int(row[3]*frame_resized.shape[0])
            conf = row[4]
            label = model.names[int(labels[i])]
            color = (0, 255, 0)
            cv2.rectangle(frame_resized, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame_resized, f'{label} {conf:.2f}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
    return cv2.cvtColor(frame_resized, cv2.COLOR_RGB2BGR)

rtsp_url = 'rtmp://192.168.10.152/live'
cap = cv2.VideoCapture(rtsp_url)
frame_count = 0
process_every_n_frames = 5  # Adjust based on performance and requirements

try:
    if not cap.isOpened():
        logging.error("Failed to open video stream.")
        exit()
    logging.info("Video stream opened successfully.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            logging.error("No frame retrieved from the stream.")
            break

        if frame_count % process_every_n_frames == 0:
            frame = process_frame(frame)
        else:
            frame = cv2.resize(frame, (640, 480))  # Maintain consistent frame size
        
        cv2.imshow("Frame", frame)
        frame_count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    logging.info("Script interrupted by user.")
finally:
    cap.release()
    cv2.destroyAllWindows()
    logging.info("Resources released and script terminated.")



try:
    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        logging.error("Failed to open video stream.")
        exit()
    logging.info("Video stream opened successfully.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            logging.error("No frame retrieved from the stream.")
            break
        
        # Directly display the frame without processing
        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    logging.info("Script interrupted by user.")
finally:
    cap.release()
    cv2.destroyAllWindows()
    logging.info("Resources released and script terminated.")
