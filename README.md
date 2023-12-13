# Jetson_FC
# Autonomous Robot Navigation System

## Overview
This code is designed for an autonomous robot navigation system using the JetBot platform. It employs computer vision techniques to enable the robot to follow a black line and make decisions when encountering a green square. The system uses a camera to capture real-time video feed, processes the images to detect specific objects, and controls the robot's movements accordingly.

## Prerequisites
- JetBot Robot Kit
- JetBot Camera
- OpenCV for Python
- IPython display tools
- Traitlets Python library

## Setup
1. Assemble your JetBot robot kit following the manufacturer's instructions.
2. Install the necessary Python libraries (`cv2`, `numpy`, `ipywidgets`, `traitlets`) if not already available.

## How It Works
1. **Camera Initialization**: The robot's camera is initialized to capture a video feed.
2. **Image Processing**: The video feed is continuously processed to identify the center of a black line and the position of a green square (if present).
3. **Decision Making**: Based on the processed image, the robot decides to either follow the black line or turn left/right when encountering a green square.
4. **Motor Control**: The robot's motors are controlled to execute the decided actions (moving forward, turning left/right).

### Key Functions
- `find_black_object_center(img)`: Identifies the center of a black object in the image.
- `find_green_square(img, black_line_center)`: Detects a green square in the image and determines its position relative to the black line.
- `update(change)`: Main loop that captures the camera feed, processes the image, and controls the robot's movements.

## Usage
1. Power on your JetBot and ensure the camera is correctly attached.
2. Run the provided Python script on your JetBot.
3. Place the JetBot on a track with a black line and optional green squares.
4. The JetBot will start following the black line, making turns at green squares.

## Customization
- Adjust HSV values in `find_green_square` to accurately detect the specific shade of green used.
- Modify `turn_duration`, `left_motor_speed`, and `right_motor_speed` in `update` to customize the robot's turning behavior.
- Change `cooldown_time` to control how frequently the robot can make turns.

## Note
- Ensure that your environment (lighting, background, etc.) is suitable for the vision system to accurately detect the black line and green squares.
- Fine-tune the HSV values and other parameters for optimal performance in your specific setting.

## Author
- Omar El Herraoui, Ahmad Fraij, Flavia Trotolo 
