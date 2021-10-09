import cv2
from src.ocr import __MIN_COLOR_VALUE__, __MAX_COLOR_VALUE__
from src.ocr.image_noise_filter import ImageNoiseFilter


# This class can filter image with color
class ImageColorFilter:
    @staticmethod
    def image_to_gray(img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert image to gray

    @staticmethod
    def invert_gray_color(gray):
        return __MAX_COLOR_VALUE__ - gray

    @staticmethod
    def image_to_canny_edge(img):
        img = ImageColorFilter.image_to_gray(img)
        img = ImageColorFilter.color_gaussian_adaptive_threshold(img)
        for index in range(0, 15):
            img = ImageNoiseFilter.noise_erode(img, 4)
            img = ImageNoiseFilter.noise_dilate(img, 3)
        return cv2.Canny(img, 40, 160)

    @staticmethod
    def color_binary_threshold(img, thresh=__MIN_COLOR_VALUE__, max_val=__MAX_COLOR_VALUE__):
        __, result = cv2.threshold(src=img, thresh=thresh, maxval=max_val, type=cv2.THRESH_BINARY)
        return result

    @staticmethod
    def color_otsu_threshold(img, thresh=__MIN_COLOR_VALUE__, max_val=__MAX_COLOR_VALUE__):
        __, result = cv2.threshold(src=img, thresh=thresh, maxval=max_val, type=cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        return result

    @staticmethod
    def color_mean_adaptive_threshold(img, block_size=11, subtracted=9):
        return cv2.adaptiveThreshold(src=img,
                                     maxValue=__MAX_COLOR_VALUE__,
                                     adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C,
                                     thresholdType=cv2.THRESH_BINARY,
                                     blockSize=block_size,
                                     C=subtracted)

    @staticmethod
    def color_gaussian_adaptive_threshold(img, block_size=35, subtracted=9):
        return cv2.adaptiveThreshold(src=img,
                                     maxValue=__MAX_COLOR_VALUE__,
                                     adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     thresholdType=cv2.THRESH_BINARY,
                                     blockSize=block_size,
                                     C=subtracted)
