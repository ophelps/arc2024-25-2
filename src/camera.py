import picamera2
import time
import cv2


camera = None
arucoDetector = None

def init(res:tuple=(1920, 1080)):
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


def get_tags():
    while True:
        image = camera.capture_array()
        corners, ids, _ = arucoDetector.detectMarkers(image)

        cv2.imshow("frame", image)
        if cv2.waitKey(10) == ord("q"):
            cv2.destroyAllWindows()
            break
        print(ids)
        print(corners)
        

init()
get_tags()