import cv2


# This script can blur image using opencv
def blur(img, size=5):
    return cv2.blur(img, (size, size))


def blur_gaussian(img, size=5):
    return cv2.GaussianBlur(img, (size, size), 0)


def blur_median(img, size=5):
    return cv2.medianBlur(img, size)


def blur_bilateral(img):
    return cv2.bilateralFilter(img, 15, 40, 45)
