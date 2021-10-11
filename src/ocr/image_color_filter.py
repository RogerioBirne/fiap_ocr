import cv2
from src.ocr import __MIN_COLOR_VALUE__, __MAX_COLOR_VALUE__
from src.ocr import image_noise_filter
from src.ocr import image


# This script can filter image with color
def image_to_gray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert image to gray


def invert_gray_color(gray):
    return __MAX_COLOR_VALUE__ - gray


def color_binary_threshold(img, thresh=__MIN_COLOR_VALUE__, max_val=__MAX_COLOR_VALUE__):
    __, result = cv2.threshold(src=img, thresh=thresh, maxval=max_val, type=cv2.THRESH_BINARY)
    return result


def color_otsu_threshold(img, thresh=__MIN_COLOR_VALUE__, max_val=__MAX_COLOR_VALUE__):
    __, result = cv2.threshold(src=img, thresh=thresh, maxval=max_val, type=cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return result


def color_mean_adaptive_threshold(img, block_size=11, subtracted=9):
    return cv2.adaptiveThreshold(src=img,
                                 maxValue=__MAX_COLOR_VALUE__,
                                 adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C,
                                 thresholdType=cv2.THRESH_BINARY,
                                 blockSize=block_size,
                                 C=subtracted)


def color_gaussian_adaptive_threshold(img, block_size=35, subtracted=9):
    return cv2.adaptiveThreshold(src=img,
                                 maxValue=__MAX_COLOR_VALUE__,
                                 adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 thresholdType=cv2.THRESH_BINARY,
                                 blockSize=block_size,
                                 C=subtracted)


def image_to_canny_edge(img, color_threshold_filter=color_otsu_threshold):
    img = image_to_gray(img)
    img = color_threshold_filter(img)
    for __ in range(15):
        img = image_noise_filter.noise_erode(img, 4)
        img = image_noise_filter.noise_dilate(img, 3)
    return cv2.Canny(img, 40, 160)
