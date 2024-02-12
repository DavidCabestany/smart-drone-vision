# Smart Drone Vision with YOLOv5

Welcome to the Smart Drone Vision project, where we integrate cutting-edge object detection technology using YOLOv5 into drone video streams. This project allows drones to recognize and classify objects in real-time, making it perfect for applications ranging from environmental monitoring to enhancing security systems.

## Project Overview

This project uses YOLOv5, a state-of-the-art object detection model, to analyze video streams captured by drones. It identifies objects within the video frame, annotates them with bounding boxes, and displays the processed video stream in real-time, complete with object labels and confidence scores.

## Features

- Real-time object detection in drone video streams
- Support for multiple YOLOv5 models (e.g., yolov5s, yolov5m, yolov5l, yolov5x)
- Customizable confidence threshold for object detection
- Display of real-time Frames Per Second (FPS) to monitor performance
- Error handling for robust execution

## Getting Started

### Prerequisites

- Python 3.8 or later
- pip (Python package installer)

### Installation

1. **Clone the Repository**

git clone https://github.com/yourusername/smart-drone-vision.git
cd smart-drone-vision

r
Copy code

2. **Set Up a Python Virtual Environment (Optional but Recommended)**

- Create the virtual environment:
  ```
  python -m venv venv
  ```
- Activate the virtual environment:
  - On Windows:
    ```
    .\venv\Scripts\activate
    ```
  - On macOS/Linux:
    ```
    source venv/bin/activate
    ```

3. **Install Dependencies**

pip install -r requirements.txt

markdown
Copy code

### Configuration

1. **Environment Variables**: Create a `.env` file in the project root directory with the following variables:
DRONE_NAME=your_drone_name
OUTPUT_DIR=output_videos
STREAM_URL=rtmp://your_stream_url/live

vbnet
Copy code
Replace the placeholder values with your actual drone name, desired output directory for saved videos, and the RTMP stream URL of your drone's video feed.

2. **Model Selection**: The code defaults to using `yolov5s` for object detection. To use a different model variant, update the `model_name` variable in the script accordingly.

## Usage

To start object detection on your drone's video stream, ensure your drone is streaming to the specified RTMP URL, then run:

python object_detection.py

css
Copy code

The script will process the video stream in real-time, display the annotated video, and save it to the specified output directory.

## Contributing

Contributions to improve Smart Drone Vision are welcome. Please feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The YOLOv5 team for providing an efficient and powerful object detection model.
- The drone community for inspiring this project.