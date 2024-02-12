from datetime import datetime
import torch
import cv2
import logging
import time
import os
from dotenv import load_dotenv
from tqdm import tqdm


print(torch.__version__)

print(torch.cuda.is_available())
print(
    torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CUDA not available"
)


# Load environment configurations
load_dotenv()
drone = os.getenv("DRONE_NAME", "your_drone")
output_dir = os.getenv("OUTPUT_DIR", "output_videos")
video_path = os.getenv(
    "VIDEO_PATH", "path_to_your_video_file.mp4"
)  # Path to your recorded video


if torch.cuda.is_available():
    logging.info(f"CUDA is available. Using GPU: {torch.cuda.get_device_name(0)}")
    device = torch.device("cuda:0")
else:
    logging.error("CUDA is not available. Exiting...")
    exit()


model_repository = "ultralytics/yolov5"
model_name = "yolov5x"


if not os.path.exists(output_dir):
    os.makedirs(output_dir)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.info(f"Starting object detection with {model_name} on recorded video!")

try:
    torch.hub._validate_not_a_forked_repo = (
        lambda a, b, c: True
    )  # Bypass local cache issue
    model = torch.hub.load("ultralytics/yolov5", "yolov5x", pretrained=True).to(device)

    model.conf = 0.45
    logging.info(f"{model_name} model loaded successfully.")
except Exception as e:
    logging.error(f"Failed to load model: {e}")
    exit()


def resize_image(image, stride=32):
    new_width = (
        (image.shape[1] // stride + 1) * stride
        if image.shape[1] % stride != 0
        else image.shape[1]
    )
    new_height = (
        (image.shape[0] // stride + 1) * stride
        if image.shape[0] % stride != 0
        else image.shape[0]
    )
    resized_image = cv2.resize(image, (new_width, new_height))
    return resized_image


results = None


def detect_objects(frame, update_detection):
    global results
    if update_detection:
        # Resize frame to match model's expected dimensions
        frame = resize_image(frame)

        # Convert frame to tensor and move to GPU
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame_tensor = (
            torch.from_numpy(frame_rgb).to(device).unsqueeze(0)
        )  # Add batch dimension and move to GPU

        frame_tensor = frame_tensor.permute(
            0, 3, 1, 2
        )  # Change dimension order to NCHW
        frame_tensor = frame_tensor.float() / 255.0  # Normalize to [0, 1]
        print(frame_tensor.shape)
        # Perform inference
        results = model(frame_tensor)

        # Check if 'results' has the 'render' method
        if hasattr(results, "render"):
            # Convert results to CPU for OpenCV compatibility and render detections
            frame_bgr = cv2.cvtColor(results.render()[0], cv2.COLOR_RGB2BGR)
        else:
            print("The 'results' object does not have a 'render' method.")
            # Handle the case where results does not have the 'render' method
            # This might involve logging an error or taking some other action

            # Convert results to CPU for OpenCV compatibility
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
processed_output_filename = f"{drone}_{model_name}_PROC_{current_time}.avi"
unprocessed_output_filename = f"{drone}_{model_name}_UNPROC_{current_time}.avi"
proc_file_path = os.path.join(output_dir, processed_output_filename)
unproc_file_path = os.path.join(output_dir, unprocessed_output_filename)

fourcc = cv2.VideoWriter_fourcc(*"XVID")
proc_out = cv2.VideoWriter(
    proc_file_path, fourcc, source_fps, (frame_width, frame_height)
)
unproc_out = cv2.VideoWriter(
    unproc_file_path, fourcc, source_fps, (frame_width, frame_height)
)

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

        if cv2.waitKey(1) & 0xFF == ord("q"):
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
    logging.info(f"Unprocessed video saved to: {os.path.abspath(unproc_file_path)}")
