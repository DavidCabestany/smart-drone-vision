import cv2
import numpy as np

# Create a dummy video stream (10 frames of random noise)
height, width = 480, 640
video = np.random.randint(0, 256, (120, height, width, 3), dtype=np.uint8)

# Initialize VideoWriter
fourcc = cv2.VideoWriter_fourcc(*'avc1')
out = cv2.VideoWriter('test_avc1.mp4', fourcc, 60.0, (width, height))

# Write the video
for frame in video:
    out.write(frame)

# Release the VideoWriter
out.release()

print("Test video written with 'avc1' codec.")
