from datetime import datetime
import torch
import cv2
import numpy as np
import logging
from imutils.video import VideoStream
import time
import os
from dotenv import load_dotenv

# Setup logging and output directory
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Use environment variables for output directory and RTMP URL
drone = os.getenv('DRONE_NAME', 'unknown')
output_dir = os.getenv('OUTPUT_DIR', 'output') 
stream_url = os.getenv('STREAM_URL', 'rtmp://IP_from_Mona_Server/live') 


if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load the YOLOv5 model
try:
    model = torch.hub.load('ultralytics/yolov5', 'yolov5l', pretrained=True)
    model.conf = 0.25  # Set a custom confidence threshold
    logging.info("YOLOv5 model loaded successfully.")
except Exception as e:
    logging.error(f"Failed to load model: {e}")
    exit()

def process_frame(frame):
    # Convert frame from BGR to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = model(frame_rgb)
    
    # Convert frame back to BGR from RGB
    frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
    
    # Parse the results
    for i in range(results.xyxy[0].shape[0]):
        # Extract coordinates for bounding box
        x1, y1, x2, y2 = map(int, results.xyxy[0][i][:4])
        # Get the confidence score and the class label
        conf = results.xyxy[0][i][4].item()
        label = int(results.xyxy[0][i][5].item())
        label_name = model.names[label]
        
        # Draw bounding box and label with confidence score
        cv2.rectangle(frame_bgr, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame_bgr, f'{label_name} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    return frame_bgr


# Start the Stream  through RTSP
 
vs = VideoStream(stream_url).start()
time.sleep(2.0)

# Output video file naming
current_time = datetime.now().strftime("%Y_%m%d_%H%M_%S")
output_filename = f"dji_mini2se_{current_time}.avi"
output_path = os.path.join(output_dir, output_filename)

# Initialize VideoWriter
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = None

frame_count = 0
detection_interval = 5  # Perform detection every 5 frames

try:
    while True:
        frame = vs.read()
        if frame is None:
            logging.error("Received an empty frame. End of stream?")
            break

        if frame_count % detection_interval == 0:
            processed_frame = process_frame(frame)
        
        if out is None:
            # Initialize the video writer after the first frame is available
            height, width = frame.shape[:2]
            out = cv2.VideoWriter(output_path, fourcc, 20.0, (width, height))
        
        out.write(processed_frame)  # Write processed frame to output file
        cv2.imshow("Frame", processed_frame)
        
        frame_count += 1  # Increment the frame count

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    logging.info("Script interrupted by user.")
finally:
    vs.stop()
    if out is not None:
        out.release()
    cv2.destroyAllWindows()
    logging.info(f"Video stream stopped, output saved to {output_filename}, and resources released.")
