from datetime import datetime
import torch
import cv2
import logging
from imutils.video import VideoStream
import time
import os
from dotenv import load_dotenv

# Load environment configurations
load_dotenv()
drone = os.getenv('DRONE_NAME', 'your_drone')
output_dir = os.getenv('OUTPUT_DIR', 'output_videos') 
stream_url = os.getenv('STREAM_URL', 'rtmp://your_stream_url/live')

model_repository = 'ultralytics/yolov5'
model_name = 'yolov5s' # 'yolov5n' 'yolov5m' 'yolov5l' 'yolov5x'

# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info(f"Starting object detection with {model_name} on drone video stream!")

try:
    model = torch.hub.load(model_repository, model_name, pretrained=True)
    model.conf = 0.25  # Custom confidence threshold
    logging.info(f"{model_name} model loaded successfully.")
except Exception as e:
    logging.error(f"Failed to load model: {e}")
    exit()

def detect_objects(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = model(frame_rgb)
    frame_bgr = cv2.cvtColor(results.render()[0], cv2.COLOR_RGB2BGR)
    return frame_bgr

# Start video stream
vs = VideoStream(stream_url).start()
time.sleep(2.0)  # Warm-up time

current_time = datetime.now().strftime("%Y_%m%d_%H%M_%S")
# Names for both processed and unprocessed video files
processed_output_filename = f"{drone}_{model_name}_processed_{current_time}.avi"
unprocessed_output_filename = f"{drone}_{model_name}_unprocessed_{current_time}.avi"
processed_output_path = os.path.join(output_dir, processed_output_filename)
unprocessed_output_path = os.path.join(output_dir, unprocessed_output_filename)

fourcc = cv2.VideoWriter_fourcc(*'XVID')

# Initialize video writer variables for both processed and unprocessed videos
processed_out = None
unprocessed_out = None

frame_count = 0
detection_interval = 5

prev_time = time.time()

try:
    while True:
        frame = vs.read()
        if frame is None:
            logging.error("Empty frame received. End of stream?")
            break

        processed_frame = detect_objects(frame) if frame_count % detection_interval == 0 else frame
        
        # Calculate FPS for display purposes
        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time

        # Display FPS on the processed frame
        cv2.putText(processed_frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Initialize video writers with the correct frame dimensions
        if processed_out is None or unprocessed_out is None:
            height, width = frame.shape[:2]
            processed_out = cv2.VideoWriter(processed_output_path, fourcc, 20.0, (width, height))
            unprocessed_out = cv2.VideoWriter(unprocessed_output_path, fourcc, 20.0, (width, height))

        # Write frames to both video files
        unprocessed_out.write(frame)  # Save original frame to unprocessed video
        processed_out.write(processed_frame)  # Save processed frame to processed video
        
        cv2.imshow("Detected Objects", processed_frame)  # Display the processed frame
        
        frame_count += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    logging.info("Interrupted by user.")
finally:
    vs.stop()
    if processed_out:
        processed_out.release()
    if unprocessed_out:
        unprocessed_out.release()
    cv2.destroyAllWindows()
    logging.info(f"Stream ended. Output saved to {processed_output_filename} and {unprocessed_output_filename}.")
