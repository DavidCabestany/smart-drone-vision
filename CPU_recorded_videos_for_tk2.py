from datetime import datetime
import torch
import cv2
import logging
import time
import os
from dotenv import load_dotenv, find_dotenv
from tqdm import tqdm  # Import tqdm for the progress bar

# Load environment configurations
load_dotenv()
dotenv_path = find_dotenv()
print(f"Attempting to load .env file from: {dotenv_path}")
drone = os.getenv('DRONE_NAME', 'your_drone')
output_dir = os.getenv('OUTPUT_DIR', 'output_videos')
video_path = os.getenv('VIDEO_PATH', 'path_to_your_video_file.mp4')  # Path to your recorded video

model_repository = 'ultralytics/yolov5'  # 'ultralytics/yolov5' or 'yolov5/models' for official YOLOv5 models
model_name = 'yolov5x'  # Choose the model size according to your needs

print(f"drone: {drone}", f"output_dir: {output_dir}", f"video_path: {video_path}", f"model_repository: {model_repository}", f"model_name: {model_name}", sep='\n')
# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info(f"Starting object detection with {model_name} on recorded video!")

try:
    model = torch.hub.load(model_repository, model_name, pretrained=True)
    model.conf = 0.45
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

# Open the recorded video
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    logging.error("Error opening video file.")
    exit()

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
source_fps = cap.get(cv2.CAP_PROP_FPS)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

current_time = datetime.now().strftime("%d_%H%M")
processed_output_filename = f"{drone}_{model_name}_PROC_{current_time}.mp4"
unprocessed_output_filename = f"{drone}_{model_name}_UNPROC_{current_time}.mp4"
proc_file_path = os.path.join(output_dir, processed_output_filename)
unproc_file_path = os.path.join(output_dir, unprocessed_output_filename)

fourcc = cv2.VideoWriter_fourcc(*'avc1')
proc_out = cv2.VideoWriter(proc_file_path, fourcc, source_fps, (frame_width, frame_height))
# unproc_out = cv2.VideoWriter(unproc_file_path, fourcc, source_fps, (frame_width, frame_height))

detection_interval = 1

# Create a tqdm progress bar
pbar = tqdm(total=total_frames, desc="Processing Frames")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            logging.info("End of video file reached.")
            break

        update_detection = (total_frames % detection_interval) == 0
        processed_frame = detect_objects(frame, update_detection)

        # unproc_out.write(frame)  # Save original frame to unprocessed video
        proc_out.write(processed_frame)  # Save processed frame to processed video

        pbar.update(1)  # Update the progress bar by one step

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    logging.info("Interrupted by user.")
finally:
    cap.release()
    proc_out.release()
    # unproc_out.release()
    cv2.destroyAllWindows()
    pbar.close()  # Close the progress bar

    # Log the full path of the output files
    logging.info(f"Video processing concluded.")
    logging.info(f"Processed video saved to: {os.path.abspath(proc_file_path)}")
    # logging.info(f"Unprocessed video saved to: {os.path.abspath(unproc_file_path)}")
