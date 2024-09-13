# ASL Hand Recognition

Welcome to ASL Hand Recognition!

## Project Overview

This project demonstrates real-time ASL Hand Recognition using a pre-trained YOLO V8 model. The application captures video from your webcam and processes each frame to detect hand gestures. The detected hands are highlighted with bounding boxes, and the class names are displayed on the screen.

## Features

- Real-time ASL Hand Recognition using a webcam
- Easy-to-use web interface
- Start and stop Recognition with the click of a button
- Display detected hands with bounding boxes and class names
- Ability to upload images for Recognition

## How it Works

The system employs a deep learning model specifically trained to recognize American Sign Language (ASL) gestures. The model is loaded using the Ultralytics YOLO library. When the Recognition is started, frames from the webcam are continuously processed by the model. Each frame is analyzed, and the model predicts the bounding boxes and class labels for the detected hands. The results are then displayed in real-time on the web interface.

## Steps to Use

1. Navigate to the Recognition page using the menu.
2. Click the "Start Recognition" button to begin capturing video from your webcam and detecting hands.
3. View the live feed with detected hands highlighted on the screen.
4. Click the "Stop Recognition" button to stop capturing video and release the webcam.
5. Additionally, you can upload images for Recognition by visiting the Upload page and selecting an image file.

## Technologies Used

- Python for backend logic
- Flask for the web framework
- OpenCV for video capture and processing
- Ultralytics YOLO V8 for the hand Recognition model
- Bootstrap for responsive and aesthetic web design
