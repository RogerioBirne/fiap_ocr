import cv2
from src.ocr import __COLOR_WHITE_RGB__, __COLOR_BLACK_RGB__
from src.ocr import image
from src.ocr import image_noise_filter
from src.ocr import image_color_filter
from src.ocr import image_contour_filter


# This script can erase a qr code inside the image
def erase_qrcode(img, margin=0):
    min_qr_code_area = int(img.shape[1] * 0.25) ** 2
    max_qr_code_area = int(img.shape[1] * 0.40) ** 2

    invert = image_color_filter.invert_gray_color(img)
    for __ in range(4):
        invert = image_noise_filter.noise_dilate(invert, 5)
    contours = image_contour_filter.find_contours(invert)
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.06 * peri, True)
        x, y, w, h = cv2.boundingRect(approx)
        area = cv2.contourArea(c)
        ar = w / float(h)
        sides = len(approx)
        if 2 <= sides <= 4 and min_qr_code_area < area < max_qr_code_area and (0.85 < ar < 1.6):
            img = image.draw_box(img, (x - margin, y - margin), (x + w + margin, y + h + margin),
                                 color=__COLOR_WHITE_RGB__, border_size=cv2.FILLED)
    return img
