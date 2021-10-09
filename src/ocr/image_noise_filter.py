import numpy as np
import cv2


# This class can filter noise using opencv
class ImageNoiseFilter:
    @staticmethod
    def noise_erode(img, sensitivity=3):
        return cv2.erode(src=img, kernel=np.ones((sensitivity, sensitivity), np.uint8))

    @staticmethod
    def noise_dilate(img, sensitivity=3):
        return cv2.dilate(src=img, kernel=np.ones((sensitivity, sensitivity), np.uint8))

    @staticmethod
    def noise_opening(img, sensitivity=3):
        erode = ImageNoiseFilter.noise_erode(img, sensitivity)
        dilate = ImageNoiseFilter.noise_dilate(erode, sensitivity)
        return dilate

    @staticmethod
    def noise_closure(img, sensitivity=3):
        dilate = ImageNoiseFilter.noise_dilate(img, sensitivity)
        erode = ImageNoiseFilter.noise_erode(dilate, sensitivity)
        return erode
