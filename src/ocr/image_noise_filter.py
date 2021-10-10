import numpy as np
import cv2


# This script can filter noise using opencv
def noise_erode(img, sensitivity=3):
    return cv2.erode(src=img, kernel=np.ones((sensitivity, sensitivity), np.uint8))


def noise_dilate(img, sensitivity=3):
    return cv2.dilate(src=img, kernel=np.ones((sensitivity, sensitivity), np.uint8))


def noise_opening(img, sensitivity=3):
    erode = noise_erode(img, sensitivity)
    dilate = noise_dilate(erode, sensitivity)
    return dilate


def noise_closure(img, sensitivity=3):
    dilate = noise_dilate(img, sensitivity)
    erode = noise_erode(dilate, sensitivity)
    return erode
