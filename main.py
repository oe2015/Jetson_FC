import cv2
import numpy as np
from jetbot import Robot, Camera
import ipywidgets.widgets as widgets
from IPython.display import display
import traitlets
from jetbot import bgr8_to_jpeg
import time

# Create robot instance
robot = Robot()

# Create and display Image widget
image_widget = widgets.Image(format='jpeg', width=300, height=300)
display(image_widget)

# Create camera instance
camera = Camera.instance()

# Function to process the image and return the center of the black object
def find_black_object_center(img):
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   
    # Apply threshold to get binary image
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
       
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
   
    if contours:
        # Find the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
       
        # Get the center of the contour
        M = cv2.moments(largest_contour)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            return (cx, cy), thresh
    return None, thresh

def find_green_square(img, black_line_center):
    # Convert the image from BGR to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
   
    # Define the range of green color in HSV
    # These values should be adjusted based on the green you want to detect
    lower_green = np.array([35, 100, 25])  # Lower end of the HSV range for green
    upper_green = np.array([80, 255, 255])  # Upper end of the HSV range for green

    # Create a mask for the green color
    mask = cv2.inRange(hsv, lower_green, upper_green)
       
    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   
    # Assume we're only interested in the largest contour
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        contour_area = cv2.contourArea(largest_contour)

        # Define a minimum area for the contour to be considered a valid green square
        min_area = 0  # This is an arbitrary value; adjust based on your image

        if contour_area > min_area:
            # Calculate the center of the bounding box
            box_center = x + w / 2
           
            # Determine if the box is on the left or right side of the black line
            if box_center < black_line_center:
                return 'left', mask
            else:
                return 'right', mask

    return None, mask
# Add a flag to control image processing
process_images = True
cooldown_time = 3  # in seconds
last_turn_time = 0.0

def update(change):
    global process_images,last_turn_time  # Declare the flag as a global variable
    image = change['new']
   
     # Check if image processing is allowed
    if not process_images:
        return
   
    # Crop the image (for example, cropping the center 150x150 pixels)
    height, width = image.shape[:2]
    crop_size = 175
    crop_box = ((width - crop_size) // 2, (height - crop_size) // 2, (width + crop_size) // 2, (height + crop_size) // 2)
    cropped_image = image[crop_box[1]:crop_box[3], crop_box[0]:crop_box[2]]

    # Process the cropped image to find the black line and green square
    center, processed_image = find_black_object_center(cropped_image)
   
    # Ensure that cx has a valid value before using it
    if center is not None:
        cx, cy = center
        green_direction, green_mask = find_green_square(cropped_image, cx)
       
        # Overlay the green mask on the processed image for visual feedback
        processed_image = cv2.bitwise_or(processed_image, green_mask)
        # Set the flag to pause image processing during the turn
       
   
        # Display the processed image
        image_widget.value = cv2.imencode('.jpg', processed_image)[1].tobytes()
   
        if green_direction == 'left' or green_direction == 'right':
            print(green_direction)
            # Set the desired turn duration and motor speeds
            turn_duration = 0.3  # in seconds
            left_motor_speed = 0.2 if green_direction == 'left' else 0.5
            right_motor_speed = 0.3 if green_direction == 'left' else 0.2

            # Set the flag to pause image processing during the turn
            process_images = False

            # Calculate the time interval for each iteration of the loop
            time_interval = 0.01  # in seconds

            # Calculate the number of iterations based on the time interval
            num_iterations = int(turn_duration / time_interval)

            try:
                if time.time() - last_turn_time > cooldown_time:
                    # Perform a smooth turn using a time-based loop
                    for i in range(num_iterations):
                        progress = i / num_iterations
                        current_left_speed = left_motor_speed * (1 - progress)
                        current_right_speed = right_motor_speed * (1 - progress)
                        robot.set_motors(current_left_speed, current_right_speed)
                        time.sleep(time_interval)
                    last_turn_time = time.time()

            finally:
                # Stop the robot after the turn is complete
                robot.stop()
                process_images = True

           

        else:
#             process_images = True
        # Process the image if enough time has passed since the last turn

            # If no green square is detected, follow the line
            if cx < int(crop_size * 0.2):  # Line is to the left (adjusted for cropped image size)
                robot.left(0.2)
            elif cx > int(crop_size * 0.6):  # Line is to the right (adjusted for cropped image size)
                robot.right(0.18)
            else:
                robot.forward(0.17)
    else:
        robot.forward(0.14)

# Link the camera output to the update function
camera_link = traitlets.dlink((camera, 'value'), (image_widget, 'value'), transform=bgr8_to_jpeg)
camera.observe(update, names='value')

# Add a delay between frames (adjust the duration based on your needs)
time.sleep(0.01)
