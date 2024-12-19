import pickle
import cv2
import numpy

with open("calibration.pkl", "rb") as file:
    calibration_data = pickle.load(file)

#https://stackoverflow.com/questions/75750177/solve-pnp-or-estimate-pose-single-markers-which-is-better
def get_marker_distance(corners, marker_size, mtx, distortion):
    marker_points = numpy.array([[-marker_size / 2, marker_size / 2, 0],
                              [marker_size / 2, marker_size / 2, 0],
                              [marker_size / 2, -marker_size / 2, 0],
                              [-marker_size / 2, -marker_size / 2, 0]], dtype=numpy.float32)
    
    success, rotation_vector, translation_vector = cv2.solvePnP(marker_points, corners, mtx, distortion, False, cv2.SOLVEPNP_IPPE_SQUARE)

    translation_vector = [int(pos[0] * 1000) / 1000 for pos in translation_vector]
    translation_vector = (translation_vector[1], translation_vector[0])

    #rotation_vector = [int(angle[0] * 10) / 10 for angle in rotation_vector]
    #rotation = rotation_vector[2]

    return translation_vector#, rotation


def get_calibration_data():
    return calibration_data