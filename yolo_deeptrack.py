import os
import cv2
import numpy as np
from tqdm import tqdm
from deep_sort.application_util import preprocessing
from deep_sort.deep_sort import nn_matching
from deep_sort.deep_sort.tracker import Tracker
from deep_sort.application_util import visualization
from deep_sort.deep_sort import detection as Detection
from deep_sort.tools import generate_detections as gdet


# Initialize deep sort.
max_cosine_distance = 0.3
nn_budget = None
metric = nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget)
tracker = Tracker(metric)

# YOLO Setup
net = cv2.dnn.readNet("./darknet/cfg/yolov7-tiny.weights", "./darknet/cfg/yolov7-tiny.cfg")
layer_names = net.getLayerNames()
output_layers_indices = net.getUnconnectedOutLayers()
output_layers = [layer_names[i[0] - 1] if isinstance(i, np.ndarray) else layer_names[i - 1] for i in output_layers_indices]
classes = [line.strip() for line in open("./darknet/data/coco.names")]

# DeepSORT setup
max_cosine_distance = 0.7
nn_budget = None
nms_max_overlap = 1.0
model_filename = 'path_to_your_model_file/mars-small128.pb'  # Adjust this path
encoder = gdet.create_box_encoder(model_filename, batch_size=1)
metric = nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget)
tracker = Tracker(metric)


def process_frame(frame):
    orig_height, orig_width, channels = frame.shape
    yolo_input_size = (640, 640)
    yolo_input = cv2.resize(frame, yolo_input_size)

    blob = cv2.dnn.blobFromImage(yolo_input, 0.00392, yolo_input_size, (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    
    current_frame_objects = []
    class_ids = []
    confidences = []
    boxes = []
    
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * orig_width)
                center_y = int(detection[1] * orig_height)
                w = int(detection[2] * orig_width)
                h = int(detection[3] * orig_height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # Convert YOLO detections to format for DeepSORT
    features = encoder(frame, boxes)
    detections = [Detection(bbox, score, feature) for bbox, score, feature in zip(boxes, confidences, features)]
    
    # Update tracker with new detections
    tracker.predict()
    tracker.update(detections)

    # Call the tracker for deep SORT.
    detections = [Detection(tlwh=detection_tlwh, confidence=confidence, feature=feature) for detection_tlwh, confidence, feature in zip(boxes, confidences, class_ids)]
    tracker.predict()
    tracker.update(detections)

    # Visualization for tracks.
    for track in tracker.tracks:
        if not track.is_confirmed() or track.time_since_update > 1:
            continue 
        tlwh = track.to_tlwh()
        label = f"{track.track_id}"
        visualization.draw_track(frame, track.track_id, tlwh)

    return frame

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    base_filename = os.path.splitext(os.path.basename(video_path))[0] + f"_yolov7tiny_deeptrack"
    extension = ".avi"
    counter = 0
    
    # Specify the output directory here
    output_directory = "/home/vjspycho/Desktop/gopro_app/processed_footage/"
    
    output_filename = os.path.join(output_directory, f"{base_filename}{extension}")

    while os.path.exists(output_filename):
        counter += 1
        output_filename = os.path.join(output_directory, f"{base_filename}_{counter}{extension}")

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_filename, fourcc, 20.0, (frame_width, frame_height))
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        processed_frame = process_frame(frame)
        out.write(processed_frame)

    cap.release()
    out.release()

video_directory = 'gopro_footage'
for video_file in tqdm(os.listdir(video_directory)):
    video_path = os.path.join(video_directory, video_file)
    if video_path.lower().endswith(('.mp4', '.avi', '.mov')):
        process_video(video_path)
