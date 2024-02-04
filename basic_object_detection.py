import cv2
import numpy as np
import os

# Load YOLO
net = cv2.dnn.readNet(".backend/darknet/cfg/yolov5l.weights", "darknet/cfg/yolov5l.cfg")
layer_names = net.getLayerNames()
out_layers = net.getUnconnectedOutLayers()
output_layers = [layer_names[i[0] - 1] if isinstance(i, np.ndarray) else layer_names[i - 1] for i in out_layers]

classes = [line.strip() for line in open("./darknet/data/coco.names")]

# Process each frame from video
def process_frame(frame):
    height, width, channels = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    
    class_ids = []
    confidences = []
    boxes = []
    
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    
    for i in range(len(boxes)):
        if i in indexes:
            label = str(classes[class_ids[i]])
            confidence = confidences[i]
            color = (0, 255, 0)
            x, y, w, h = boxes[i]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 30), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
    return frame

# Load your GoPro footage
cap = cv2.VideoCapture('gopro_footage/GOPR0368.MP4')

# Define the codec and create VideoWriter object
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))


base_filename = "output_video"
extension = ".avi"
counter = 0
output_filename = f"{base_filename}{extension}"

while os.path.exists(output_filename):
    counter += 1
    output_filename = f"{base_filename}_{counter}{extension}"

fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output_filename, fourcc, fps, (frame_width, frame_height))

while True:
    ret, frame = cap.read()
    if not ret:
        break
    processed_frame = process_frame(frame)
    out.write(processed_frame)  # Write the processed frame to the video file
    cv2.imshow("Processed GoPro Footage", processed_frame)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
out.release()  # Release the VideoWriter
cv2.destroyAllWindows()