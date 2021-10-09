import cv2

from src.ocr import __DEFAULT_DEBUG__


# This class can blur image using opencv
class ImageBlur:

    def __init__(self, debug_model=__DEFAULT_DEBUG__):
        self.__debug_model = debug_model

    @staticmethod
    def blur(img, size=5):
        return cv2.blur(img, (size, size))

    @staticmethod
    def blur_gaussian(img, size=5):
        return cv2.GaussianBlur(img, (size, size), 0)

    @staticmethod
    def blur_median(img, size=5):
        return cv2.medianBlur(img, size)

    @staticmethod
    def blur_bilateral(img):
        return cv2.bilateralFilter(img, 15, 40, 45)
