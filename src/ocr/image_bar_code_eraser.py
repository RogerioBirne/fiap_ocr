import cv2
from src.ocr import __COLOR_WHITE_RGB__, __COLOR_BLACK_RGB__
from src.ocr import image
from src.ocr import image_noise_filter
from src.ocr import image_color_filter
from src.ocr import image_contour_filter

__MIN_BAR_CODE_AREA__ = 0.5
__MAX_BAR_CODE_AREA__ = 2
__MIN_BAR_Y_FACTOR__ = 0.4

__MIN_BAR_VERTICES__ = 2
__MAX_BAR_VERTICES__ = 4

__MIN_BAR_RATIO__ = 6
__MAX_BAR_RATIO__ = 10


# This script can erase a bar code inside the image
def erase_barcode(img, margin=0):
    (height, wight) = img.shape[:2]

    ref_area = height * 0.08 * wight * 0.85 * wight / height
    min_bar_code_area = ref_area * __MIN_BAR_CODE_AREA__
    max_bar_code_area = ref_area * __MAX_BAR_CODE_AREA__

    invert = image_color_filter.invert_gray_color(img)
    for __ in range(min(height // 1000, 10) * 2):
        invert = image_noise_filter.noise_dilate(invert, 5)

    contours = image_contour_filter.find_contours(invert)
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.05 * peri, True)
        x, y, w, h = cv2.boundingRect(approx)
        area = cv2.contourArea(c)
        ar = w / float(h)
        sides = len(approx)

        if y > height * __MIN_BAR_Y_FACTOR__ \
                and __MIN_BAR_VERTICES__ <= sides <= __MAX_BAR_VERTICES__ \
                and min_bar_code_area < area < max_bar_code_area \
                and __MIN_BAR_RATIO__ < ar < __MAX_BAR_RATIO__:
            start_pt = (x - margin, y - margin)
            end_pt = (x + w + margin, y + h + margin)
            return image.draw_box(img, start_pt, end_pt, color=__COLOR_WHITE_RGB__, border_size=cv2.FILLED)
    return img
