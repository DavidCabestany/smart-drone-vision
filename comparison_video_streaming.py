from datetime import datetime
import torch
import cv2
import logging
from imutils.video import VideoStream
import time
import os
from dotenv import load_dotenv
import numpy as np

# Load environment configurations
load_dotenv()
drone = os.getenv('DRONE_NAME', 'your_drone')
output_dir = os.getenv('OUTPUT_DIR', 'output_videos')
stream_url = os.getenv('STREAM_URL', 'rtmp://your_stream_url/live')

print(f"Drone: {drone}", f"Output directory: {output_dir}", f"Stream URL: {stream_url}", torch.cuda.is_available(), sep='\n')
model_repository = 'ultralytics/yolov5'
model_name = 'yolov8'  # 'yolov5n','yolov5s', 'yolov5m', 'yolov5l', 'yolov5x'

proc_out_dir = os.path.join(output_dir, 'processed_footage')
unproc_out_dir = os.path.join(output_dir, 'unprocessed_footage')

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)
os.makedirs(proc_out_dir, exist_ok=True)
os.makedirs(unproc_out_dir, exist_ok=True)

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info(f"Starting object detection with {model_name} on drone video stream!")

try:
    model = torch.hub.load(model_repository, model_name, pretrained=True).to('cuda')
    model.conf = 0.20
    logging.info(f"{model_name} model loaded successfully.")
except Exception as e:
    logging.error(f"Failed to load model: {e}")
    exit()

results = None

def detect_objects(frame, update_detection):
    global results
    if update_detection:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = model(frame_rgb)
        frame_bgr = cv2.cvtColor(results.render()[0], cv2.COLOR_RGB2BGR)
    elif results:
        frame_bgr = cv2.cvtColor(results.render()[0], cv2.COLOR_RGB2BGR)
    else:
        frame_bgr = frame
    return frame_bgr

# Initialization for FPS calculation
frame_times = []
frame_time_limit = 100  # Calculate average FPS over the last 100 frames
default_fps = 30.0

# Start video stream
vs = VideoStream(stream_url).start()
time.sleep(2.0)  # Warm-up time

current_time = datetime.now().strftime("%mm%d_%H%M")
processed_output_filename = f"{drone}_{model_name}_{current_time}.mp4"
unprocessed_output_filename = f"{drone}_{model_name}_{current_time}.mp4"
proc_file_path = os.path.join(proc_out_dir, processed_output_filename)
unproc_file_path = os.path.join(unproc_out_dir, unprocessed_output_filename)

fourcc = cv2.VideoWriter_fourcc(*'avc1')
proc_out, unproc_out = None, None
frame_count, detection_interval, frames_processed = 0, 1, 0

prev_time = time.time()


try:
    while True:
        frame = vs.read()
        if frame is None:
            logging.error("Empty frame received. End of stream?")
            break

        update_detection = frame_count % detection_interval == 0
        processed_frame = detect_objects(frame, update_detection)

        # Calculate FPS
        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time

        # Display FPS on the processed frame for reference
        cv2.putText(processed_frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        if proc_out is None or unproc_out is None:
            height, width = frame.shape[:2]
            proc_out = cv2.VideoWriter(proc_file_path, fourcc, default_fps, (width, height))
            unproc_out = cv2.VideoWriter(unproc_file_path, fourcc, default_fps, (width, height))

        # Save frames to videos
        unproc_out.write(frame)
        proc_out.write(processed_frame)

        # Resize processed frame to match the unprocessed frame size if necessary
        processed_frame_resized = cv2.resize(processed_frame, (width, height))
        
        # Concatenate frames horizontally
        combined_frame = np.hstack((frame, processed_frame_resized))

        # Display the combined frame
        cv2.imshow('Stream Comparison', combined_frame)
        
        frame_count += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    logging.info("Interrupted by user.")
finally:
    vs.stop()
    if proc_out:
        proc_out.release()
    if unproc_out:
        unproc_out.release()
    cv2.destroyAllWindows()

    # Log the outcome of the video processing
    if frame_count > 0:
        logging.info(f"Video processing session concluded successfully. The processed and unprocessed video streams have been saved as '{processed_output_filename}' and '{unprocessed_output_filename}', respectively, in the directory '{output_dir}'. A total of {frame_count} frames were analyzed and processed.")
    else:
        logging.warn("The video processing session ended without processing any frames. This could be due to an early termination of the stream or a connection issue. Please verify the stream's integrity and try again. No output files have been saved.")
