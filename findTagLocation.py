import cv2
import picamera2
import time
import numpy

import unpacking

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

# cap = cv2.VideoCapture(2)
init()

num = 0

calibration_data = unpacking.get_calibration_data()

while True:

    image = camera.capture_array()
    corners, ids, _ = arucoDetector.detectMarkers(image)

    k = cv2.waitKey(5)

    if k == 27:
        break
    

    if ids is not None:
        cv2.aruco.drawDetectedMarkers(image, corners, ids)
        for i in range(len(ids)):
            cv2.line(image,(360,210), (int((corners[i][0][0][0]+corners[i][0][2][0])/2), int((corners[i][0][0][1]+corners[i][0][2][1])/2)), 1, 4)
            
            location = unpacking.get_marker_distance(corners[i], 21 * 2.54 / 100, *calibration_data)
            cv2.putText(image,str(location),(200,210),cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
            print("TAG ID: " + str(ids[i]))
            print("LOCATION:")
            print(location)
            print("-----------------------------------------------------")


    cv2.imshow('Img',image)

# Release and destroy all windows before termination
# #cap.release()

cv2.destroyAllWindows()