import logging
import os
from datetime import datetime

import cv2
import torch
from dotenv import find_dotenv, load_dotenv
from tqdm import tqdm  # Import tqdm for the progress bar


# Function to reset specific environment variables
def reset_env_vars(var_names):
    for var_name in var_names:
        if var_name in os.environ:
            del os.environ[var_name]

# Specify environment variables you want to reset
env_vars_to_reset = ["DRONE_NAME", "OUTPUT_DIR", "VIDEO_PATH"]

# Reset specified environment variables
reset_env_vars(env_vars_to_reset)

# Now, load environment configurations
load_dotenv()
dotenv_path = find_dotenv()
print(f"Attempting to load .env file from: {dotenv_path}")

# Fetch new values from the .env file or use defaults if not specified
drone = os.getenv("DRONE_NAME", "your_drone")
output_dir = os.getenv("OUTPUT_DIR", "output_videos")
video_path = os.getenv("VIDEO_PATH", r"C:\Users\David\Desktop\IMG_7062.MOV")
weights_dir = r"C:\Users\David\Projects\smart-drone-vision\yolov5\runs\train\exp5\weights"
best_weights_path = os.path.join(weights_dir, "best.pt")  # Full path to be

print(
    f"Environment Variables after loading {dotenv_path}:", 
    f"DRONE_NAME: {drone}",
    f"OUTPUT_DIR: {output_dir}",
    f"VIDEO_PATH: {video_path}",
    f"drone: {drone}",
    f"output_dir: {output_dir}",
    f"video_path: {video_path}",
    sep="\n",
)
# Load the model with custom weights
model = torch.hub.load(
    "ultralytics/yolov5", "custom", path=best_weights_path, force_reload=True
)
model.conf = 0.1  # Set a custom confidence threshold
model_name = "custom"  # Indicate that you are using a custom model

print(
    f"weights_dir: {weights_dir}",
    f"best_weights_path: {best_weights_path}",
    f"model: {model}",
    f"model_name: {model_name}",
    sep="\n",
)

# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Initialize logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.info(f"Starting object detection with {model_name} on recorded video!")

try:
    # Load the custom model with your finetuned weights
    model = torch.hub.load(
        "ultralytics/yolov5", "custom", path=best_weights_path, force_reload=True
    )

    model.conf = 0.45  # Set the confidence threshold for detection
    logging.info(f"{model_name} model loaded with custom weights successfully.")
except Exception as e:
    logging.error(f"Failed to load model with custom weights: {e}")
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

fourcc = cv2.VideoWriter_fourcc(*"avc1")
proc_out = cv2.VideoWriter(
    proc_file_path, fourcc, source_fps, (frame_width, frame_height)
)

detection_interval = 1

pbar = tqdm(total=total_frames, desc="Processing Frames")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            logging.info("End of video file reached.")
            break

        update_detection = (total_frames % detection_interval) == 0
        processed_frame = detect_objects(frame, update_detection)

        proc_out.write(processed_frame)
        pbar.update(1)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

except KeyboardInterrupt:

    logging.info("Interrupted by user.")
finally:
    cap.release()
    proc_out.release()

    cv2.destroyAllWindows()
    pbar.close()

    logging.info(f"Video {video_path} processing concluded.")
    logging.info(f"Processed video saved to: {os.path.abspath(proc_file_path)}")
