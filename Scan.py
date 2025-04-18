import cv2
import picamera2
import time
import numpy
from pymavlink import mavutil

import Unpacking

camera = None
arucoDetector = None

def init(res:tuple=(720, 420)):
    global camera
    global arucoDetector

    camera = picamera2.Picamera2()

    config = camera.create_video_configuration(
        main={"size": res, "format": "RGB888"}, buffer_count=6
    )
    camera.configure(config)
    #camera.set_controls({"ExposureTime": Consts.EXPOSURE})
    camera.start()
    time.sleep(1)  # sleep statement to allow camera to fully wake up
    print("camera initialization complete")

    arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    arucoParams = cv2.aruco.DetectorParameters()
    arucoDetector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)

init()

num = 0

calibration_data = Unpacking.get_calibration_data()

def scan_for_tags(the_connection):
    print("Getting image")
    image = camera.capture_array()
    with open("recentImage.jpg", "w") as recentImage:
        recentImage.write(str(image))

    print("Scanning for tags")
    corners, ids, _ = arucoDetector.detectMarkers(image)
    print("Getting location of tags")
    location_actual = get_location(the_connection)
    
    if ids is None:
        return {}
    
    locations = {}
    
    print("Getting location of tags")
    for i in range(len(ids)):
        id = ids[i][0]
        if id >= 1 and id <= 3:
            location_target = Unpacking.get_marker_distance(corners[i], 21 * 2.54 / 100, *calibration_data)
            locations[id] = numpy.sum((location_target, location_actual), axis=1)
    return locations

def get_location(the_connection):
    location_message = the_connection.recv_match(type='LOCAL_POSITION_NED', blocking=True)
    location_actual = (location_message.x, location_message.y)
    #location_actual = (0, 0)
    print("GOT LOCATION: " + str(location_actual) + "meters")
    return location_actual

def get_height(the_connection):
    location_message = the_connection.recv_match(type='LOCAL_POSITION_NED', blocking=True)
    location_actual = -location_message.z
    print("GOT ALTITUDE: " + str(location_actual) + " meters")
    return location_actual

def go_to_tag(the_connection, location_target, altitude=1, tolerance=1):
    print("Navigation to tag initiated")
    the_connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, the_connection.target_system, the_connection.target_component, mavutil.mavlink.MAV_FRAME_LOCAL_NED, int(0b110111111000), *location_target, -altitude, 0, 0, 0, 0, 0, 0, 0, 0))
    location_actual = get_location(the_connection)
    print("Initializing loop")
    while not abs(location_target[0] - location_actual[0]) < tolerance/100 and not abs(location_target[1] - location_actual[1]) < tolerance/100:
        print("Still navigating to tag...")
        location_actual = get_location(the_connection)
        print("actual position: " + str(location_actual))
        print("target position: " + str(location_target))
        time.sleep(0.01)
    print("Navigation to tag complete")
