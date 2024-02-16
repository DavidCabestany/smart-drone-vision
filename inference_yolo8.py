# from ultralytics import YOLO
# model = YOLO('yolov8n.pt')  # Load the pretrained model

# source = 'path/to/image.jpg'  # Path to your image
# results = model(source)

# for box in results.boxes:
#     cords = box.xyxy[0].tolist()  # Coordinates of the bounding box
#     class_id = box.cls[0].item()  # Class ID of the detected object
#     conf = box.conf[0].item()  # Confidence score
#     print(f"Object type: {results.names[class_id]}")
#     print(f"Coordinates: {cords}")
#     print(f"Probability: {conf}")


from datetime import datetime
import cv2
import logging
from imutils.video import VideoStream
import time
import os
from dotenv import load_dotenv
import numpy as np
from ultralytics import YOLO  # Import YOLO class

# Load environment configurations
load_dotenv()
drone = os.getenv('DRONE_NAME', 'your_drone')
output_dir = os.getenv('OUTPUT_DIR', 'output_videos')
stream_url = os.getenv('STREAM_URL', 'rtmp://your_stream_url/live')

print(f"Drone: {drone}", f"Output directory: {output_dir}", f"Stream URL: {stream_url}", sep='\n')

# Model initialization
model_name = 'yolov8n'  # Choose model size (n, s, m, l, x)
model = YOLO(model_name + '.pt')  # Load the model

proc_out_dir = os.path.join(output_dir, 'processed_footage')
unproc_out_dir = os.path.join(output_dir, 'unprocessed_footage')

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)
os.makedirs(proc_out_dir, exist_ok=True)
os.makedirs(unproc_out_dir, exist_ok=True)

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info(f"Starting object detection with {model_name} on drone video stream!")

def draw_boxes(frame, detections):
    for det in detections:  # Assuming det is a tensor or a list with the detection info
        left, top, right, bottom = det['bbox']  # Adjust indexing based on actual det structure
        class_id = det['class']
        confidence = det['confidence']
        label = f"{model.names[class_id]}: {confidence:.2f}"

        # Draw rectangle
        frame = cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        # Put class label on top of rectangle
        frame = cv2.putText(frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
    return frame

def detect_objects(frame, model):
    # Convert frame to RGB for YOLOv8 compatibility if needed
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Run inference
    results = model(frame_rgb)  # This returns a list of detections
    
    # Process detections and draw boxes
    frame_with_boxes = draw_boxes(frame, results)
    
    return frame_with_boxes


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

        # Display FPS on the frame
        cv2.putText(processed_frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # Initialize VideoWriter objects if not already done
        if proc_out is None or unproc_out is None:
            height, width = frame.shape[:2]
            proc_out = cv2.VideoWriter(proc_file_path, fourcc, fps, (width, height))
            unproc_out = cv2.VideoWriter(unproc_file_path, fourcc, fps, (width, height))
        # Save frames to videos
        unproc_out.write(frame)  # Save original frame to unprocessed video
        proc_out.write(processed_frame)  # Save processed frame to processed video
        
        # Display the frames
        cv2.imshow('Processed Stream', processed_frame)


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
