import torch
import cv2
import numpy as np
import logging
from imutils.video import VideoStream
import time
import os
from datetime import datetime

# Setup logging and output directory
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load the YOLOv5 model
try:
    model = torch.hub.load('ultralytics/yolov5', 'yolov5l', pretrained=True)
    logging.info("YOLOv5 model loaded successfully.")
except Exception as e:
    logging.error(f"Failed to load model: {e}")
    exit()

def process_frame(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    try:
        results = model(frame_rgb)
        labels, cords = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
        for i in range(len(labels)):
            row = cords[i]
            x1, y1, x2, y2, conf = [int(val) for val in (row[0]*frame.shape[1], row[1]*frame.shape[0], row[2]*frame.shape[1], row[3]*frame.shape[0], row[4])]
            label = model.names[int(labels[i])]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f'{label} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    except Exception as e:
        logging.error(f"Error processing frame: {e}")
    return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

stream_url = 'rtmp://192.168.10.152/live'  # Update this URL to your stream
vs = VideoStream(stream_url).start()
time.sleep(2.0)

# Fetch the frame size dynamically
frame = vs.read()
height, width = frame.shape[:2]

# Setup VideoWriter with dynamic naming based on date and time
current_time = datetime.now().strftime("%Y_%m/%d_%H%M_%S")
output_filename = f"dji_mini2se_{current_time}.avi"
output_path = os.path.join(output_dir, output_filename)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output_path, fourcc, 20.0, (width, height))

try:
    while True:
        frame = vs.read()
        if frame is None:
            logging.error("Received an empty frame. End of stream?")
            break

        processed_frame = process_frame(frame)
        out.write(processed_frame)  # Write frame to output file

        cv2.imshow("Frame", processed_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    logging.info("Script interrupted by user.")
finally:
    vs.stop()
    out.release()
    cv2.destroyAllWindows()
    logging.info(f"Video stream stopped, output saved to {output_filename}, and resources released.")
