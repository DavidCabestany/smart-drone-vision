import torch
import cv2
import numpy as np
import logging
from imutils.video import VideoStream
import time

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
    # Resize frame for faster processing
    frame = cv2.resize(frame, (640, 480))
    # Convert frame from BGR to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    try:
        results = model(frame_rgb)
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
    
    return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

# RTSP/RTMP URL
stream_url = 'rtmp://192.168.10.152/live'  # Ensure this is your correct stream URL

# Initialize the video stream
vs = VideoStream(stream_url).start()
time.sleep(2.0)  # Allow the camera sensor to warm up

try:
    while True:
        # Read the next frame from the video stream
        frame = vs.read()

        if frame is None:
            logging.error("Received an empty frame. End of stream?")
            break

        # Process the frame for object detection and display
        processed_frame = process_frame(frame)

        cv2.imshow("Frame", processed_frame)
        
        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    logging.info("Script interrupted by user.")
finally:
    # Release the video stream and close OpenCV windows
    vs.stop()
    cv2.destroyAllWindows()
    logging.info("Video stream stopped and resources released.")
