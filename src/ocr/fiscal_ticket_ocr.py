import numpy as np
import cv2
import math
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import pytesseract
from pytesseract import Output
import imutils
from src import RESOURCES_PATH
from src.ocr import __DEFAULT_LANGUAGE__, __DEFAULT_DEBUG__, __MIN_COLOR_VALUE__, __MAX_COLOR_VALUE__
from src.ocr import __COLOR_RED_RGB__, __COLOR_GREEN_RGB__, __COLOR_BLUE_RGB__, __COLOR_BLACK_RGB__, __COLOR_WHITE_RGB__
from src.ocr.image_blur import ImageBlur
from src.ocr.image_noise_filter import ImageNoiseFilter
from src.ocr.image_color_filter import ImageColorFilter
from src.ocr.image_contour_filter import ImageContourFilter


# This class can transform a fiscal ticket image in text using tesseract and opencv
class FiscalTicketOcr:

    def __init__(self, language=__DEFAULT_LANGUAGE__,
                 debug_model=__DEFAULT_DEBUG__):
        self.__language = language
        self.__debug_model = debug_model

        tesseract_dic_path = '{}/tessdata'.format(RESOURCES_PATH)
        tesseract_psm = '6'  # Assume a single uniform block of text.
        self.__tesseract_conf = '--tessdata-dir {} --psm {}'.format(tesseract_dic_path, tesseract_psm)

    def convert_file_image_to_string(self, file, margin=0):
        self.__log_debug('Start ocr from file {}'.format(file))
        img = self.__open_image_as_bgr(file)
        return self.convert_image_to_string(img, margin=margin)

    def convert_image_to_string(self, img, margin=0):
        img = self.__convert_image_perspective(img)

        img = ImageColorFilter.image_to_gray(img)
        img = ImageColorFilter.color_gaussian_adaptive_threshold(img)

        img = self.__erase_qrcode(img, margin=25)

        img = ImageNoiseFilter.noise_closure(img)
        img = ImageNoiseFilter.noise_erode(img)

        if margin > 0:
            img = self.__remove_margin(img, margin=margin)
        self.__show_image(img, 'Fiscal ticket right to OCR')

        text = self.__convert_image_to_string(img)
        self.__log_debug(text)
        return text

    def __log_debug(self, message):
        if self.__debug_model:
            print(message)

    @staticmethod
    def __show_image(img, title='image'):
        cv2.imshow(title, img)  # Show image
        cv2.setWindowProperty(title, cv2.WND_PROP_TOPMOST, 1)
        cv2.waitKey(0)  # wait for any press
        cv2.destroyAllWindows()  # Close window

    @staticmethod
    def __open_image_as_bgr(file):
        return cv2.imread(file)  # Open Image

    @staticmethod
    def __resize(img, height, wight):
        return cv2.resize(src=img, dsize=(height, wight))

    @staticmethod
    def __enlarge(img, factor):
        return cv2.resize(src=img, dsize=None, fx=factor, fy=factor, interpolation=cv2.INTER_CUBIC)

    @staticmethod
    def __reduce(img, factor):
        return cv2.resize(src=img, dsize=None, fx=factor, fy=factor, interpolation=cv2.INTER_AREA)

    @staticmethod
    def __remove_margin(img, margin=20):
        (height, wight) = img.shape[:2]
        return img[margin:height - margin, margin:wight - margin]

    @staticmethod
    def __erase_qrcode(img, margin=0):
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

    @staticmethod
    def __convert_image_perspective(img):
        img_edge = ImageColorFilter.image_to_canny_edge(img)

        (height, wight) = img.shape[:2]
        ratio_src = height / wight

        contours = ImageContourFilter.find_contours(img_edge)

        fiscal_ticket_contour = ImageContourFilter.select_biggest_contour(contours)
        if fiscal_ticket_contour is not None:
            fiscal_ticket_contour = ImageContourFilter.sort_contour_points(fiscal_ticket_contour)
            pts1 = np.float32(fiscal_ticket_contour)
            pts2 = np.float32([[0, 0], [wight, 0], [wight, height], [0, height]])

            perspective_transform_matrix = cv2.getPerspectiveTransform(pts1, pts2)
            img = cv2.warpPerspective(img, perspective_transform_matrix, (wight, height))
            img = FiscalTicketOcr.__fix_image_ratio(img, ratio_src, fiscal_ticket_contour)
        return img

    @staticmethod
    def __fix_image_ratio(img, ratio_src, fiscal_ticket_contour):
        pt1 = fiscal_ticket_contour[0][0]
        pt2 = fiscal_ticket_contour[1][0]
        pt3 = fiscal_ticket_contour[2][0]
        pt4 = fiscal_ticket_contour[3][0]

        dist_x1 = math.sqrt((pt2[0] - pt1[0]) ** 2 + (pt2[1] - pt1[1]) ** 2)
        dist_x2 = math.sqrt((pt3[0] - pt4[0]) ** 2 + (pt3[1] - pt4[1]) ** 2)
        dist_x = (dist_x1 + dist_x2) / 2

        dist_y1 = math.sqrt((pt4[0] - pt1[0]) ** 2 + (pt4[1] - pt1[1]) ** 2)
        dist_y2 = math.sqrt((pt3[0] - pt2[0]) ** 2 + (pt3[1] - pt2[1]) ** 2)
        dist_y = (dist_y1 + dist_y2) / 2
        perspective_factor = dist_y / dist_x

        (height, wight) = img.shape[:2]
        return FiscalTicketOcr.__resize(img, height, int((height // ratio_src) * perspective_factor))

    @staticmethod
    def __draw_point(img, point, color=__COLOR_RED_RGB__):
        return cv2.circle(img, point, radius=0, color=color, thickness=20)

    @staticmethod
    def __draw_box(img, point_1, point_2, color=__COLOR_RED_RGB__, border_size=2):
        return cv2.rectangle(img, pt1=point_1, pt2=point_2, color=color, thickness=border_size)

    @staticmethod
    def __write_text(text, img, x, y, font, font_length=32):
        image_font = ImageFont.truetype(font, font_length)
        img_pil = Image.fromarray(img)
        draw = ImageDraw.Draw(img_pil)
        draw.text((x, y - font_length), text, font=image_font)
        return np.array(img_pil)

    def __convert_image_to_string(self, img):
        return pytesseract.image_to_string(img,
                                           lang=self.__language,
                                           config=self.__tesseract_conf)

    def __convert_image_to_data(self, img):
        return pytesseract.image_to_data(img,
                                         lang=self.__language,
                                         config=self.__tesseract_conf,
                                         output_type=Output.DICT)
