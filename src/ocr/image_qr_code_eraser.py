import cv2
from src.ocr import __COLOR_RED_RGB__, __COLOR_GREEN_RGB__, __COLOR_BLUE_RGB__, __COLOR_BLACK_RGB__, __COLOR_WHITE_RGB__
from src.ocr.image_noise_filter import ImageNoiseFilter
from src.ocr.image_color_filter import ImageColorFilter
from src.ocr.image_contour_filter import ImageContourFilter


# This class can erase a qr code inside the image
class ImageQrCodeEraser:
    @staticmethod
    def erase_qrcode(img, margin=0):
        invert = ImageColorFilter.invert_gray_color(img)
        invert = ImageNoiseFilter.noise_closure(invert, 21)

        contours = ImageContourFilter.find_contours(invert)
        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.06 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
            area = cv2.contourArea(c)
            ar = w / float(h)
            if len(approx) == 4 and area > 10000 and (0.85 < ar < 1.6) and w > 500 and h > 500:
                cv2.rectangle(img, (x - margin, y - margin), (x + w + margin, y + h + margin), __COLOR_WHITE_RGB__,
                              cv2.FILLED)
        return img
