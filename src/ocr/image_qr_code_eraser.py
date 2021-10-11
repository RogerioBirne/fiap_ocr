import cv2
from src.ocr import __COLOR_WHITE_RGB__
from src.ocr import image
from src.ocr import image_noise_filter
from src.ocr import image_color_filter
from src.ocr import image_contour_filter


# This script can erase a qr code inside the image
def erase_qrcode(img, margin=0):
    invert = image_color_filter.invert_gray_color(img)
    invert = image_noise_filter.noise_closure(invert, 21)

    contours = image_contour_filter.find_contours(invert)
    min_qr_code_side = int(img.shape[1] * 0.20)
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.06 * peri, True)
        x, y, w, h = cv2.boundingRect(approx)
        area = cv2.contourArea(c)
        ar = w / float(h)
        if len(approx) == 4 and area > 10000 and (0.85 < ar < 1.6) and w >= min_qr_code_side and h >= min_qr_code_side:
            img = image.draw_box(img, (x - margin, y - margin), (x + w + margin, y + h + margin),
                                 color=__COLOR_WHITE_RGB__, border_size=cv2.FILLED)
    return img
