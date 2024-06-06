# ASL Hand Detection

Welcome to ASL Hand Detection!

## Project Overview

This project demonstrates real-time ASL Hand Detection using a pre-trained model YOLO V8. The application captures video from your webcam and processes each frame to detect hand gestures. The detected hand are highlighted with bounding boxes, and the class names are displayed on the screen.

## Features

- Real-time ASL Hand Detection using a webcam
- Easy-to-use web interface
- Start and stop detection with the click of a button
- Display detected hand with bounding boxes and class names

## How it Works

The system employs a deep learning model specifically trained to recognize American Sign Language (ASL) gestures. The model is loaded using the Ultralytics YOLO library. When the detection is started, frames from the webcam are continuously processed by the model. Each frame is analyzed, and the model predicts the bounding boxes and class labels for the detected hands. The results are then displayed in real-time on the web interface.

## Steps to Use

1. Navigate to the Detection page using the menu.
2. Click the "Start Detection" button to begin capturing video from your webcam and detecting hand.
3. View the live feed with detected hands highlighted on the screen.
4. Click the "Stop Detection" button to stop capturing video and release the webcam.

## Technologies Used

- Python for backend logic
- Flask for the web framework
- OpenCV for video capture and processing
- Ultralytics YOLO V8 for the hand detection model
- Bootstrap for responsive and aesthetic web design
