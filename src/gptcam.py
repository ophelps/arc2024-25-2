import picamera2
import time
import cv2
import numpy as np

# Global variables
camera = None
arucoDetector = None

def init(res: tuple = (1920, 1080)):
    global camera, arucoDetector  # Use global variables

    # Initialize the camera
    camera = picamera2.Picamera2()

    # Create video configuration
    config = camera.create_video_configuration(
        main={"size": res, "format": "RGB888"}, buffer_count=6
    )
    camera.configure(config)
    camera.start()
    
    time.sleep(1)  # Allow the camera to fully wake up
    print("Camera initialization complete")

    # Initialize ArUco detector
    arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    arucoParams = cv2.aruco.DetectorParameters()  # Correct method to create parameters
    arucoDetector = (arucoDict, arucoParams)  # Store the dictionary and parameters tuple

def get_tags():
    global camera, arucoDetector

    # Capture an image from the camera
    image = camera.capture_array()  # Returns image as numpy array

    # Detect ArUco markers in the image
    arucoDict, arucoParams = arucoDetector  # Unpack the ArUco detector tuple
    corners, ids, rejected = cv2.aruco.detectMarkers(image, arucoDict, parameters=arucoParams)
    
    # Check if any markers were detected
    if ids is not None:
        print("Detected markers:", ids)
        return corners, ids
    else:
        print("No markers detected.")
        return None, None

def scan_for_tags():
    # Infinite loop to scan for tags continuously
    while True:
        corners, ids = get_tags()  # Capture and process the image
        
        # Optional: You can draw the markers on the image for visualization
        if corners is not None:
            # Draw detected markers on the image
            cv2.aruco.drawDetectedMarkers(capture_image, corners, ids)
            # Display the image with markers drawn
            cv2.imshow("ArUco Marker Detection", capture_image)

        # Exit loop if the user presses 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Clean up and release resources
    cv2.destroyAllWindows()

# Example usage:
init()  # Initialize the camera and ArUco detector
scan_for_tags()  # Continuously scan for ArUco tags
