import numpy as np
import cv2
import imutils


# This script look for contours on image
def find_contours(img, sort_desc=True):
    contours = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=sort_desc)[:6]
    return contours


def select_biggest_contour(contours):
    for contour, index in zip(contours, range(0, len(contours))):
        perimeter = cv2.arcLength(contour, True)
        sides = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        if len(sides) >= 4:
            return sides
    return None


def sort_contour_points(contour):
    points = contour.reshape((len(contour), 2))
    sorted_points = np.zeros((4, 1, 2), dtype=np.int32)

    add = points.sum(1)
    sorted_points[0] = points[np.argmin(add)]
    sorted_points[2] = points[np.argmax(add)]

    diff = np.diff(points, axis=1)
    sorted_points[1] = points[np.argmin(diff)]
    sorted_points[3] = points[np.argmax(diff)]
    return sorted_points
