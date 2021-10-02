import numpy as np
import cv2
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import pytesseract
from pytesseract import Output
import imutils
from src import RESOURCES_PATH

__DEFAULT_LANGUAGE__ = 'por'
__DEFAULT_DEBUG__ = False
__DEFAULT_MIN_TRUST_LEVEL__ = 0.9
__MIN_COLOR_VALUE__ = 0
__MAX_COLOR_VALUE__ = 255

__EAST_OVERLAP_THRESH__ = 0.5
__EAST_DETECTOR_DATASET__ = '{}/model/frozen_east_text_detection.pb'.format(RESOURCES_PATH)
__EAST_LAYER_NAMES__ = ['feature_fusion/Conv_7/Sigmoid', 'feature_fusion/concat_3']
__EAST_BASE_SIZE__ = 32
__EAST_ENLARGE_FACTOR__ = 2

__COLOR_RED_RGB__ = (255, 0, 0)
__COLOR_GREEN_RGB__ = (0, 255, 0)
__COLOR_BLUE_RGB__ = (0, 0, 255)
__COLOR_BLACK_RGB__ = (0, 0, 0)
__COLOR_WHITE_RGB__ = (255, 255, 255)


# This class can transform a fiscal ticket image in text using tesseract and opencv
class FiscalTicketOcr:

    def __init__(self, language=__DEFAULT_LANGUAGE__,
                 min_trust_level=__DEFAULT_MIN_TRUST_LEVEL__,
                 debug_model=__DEFAULT_DEBUG__):
        self.__language = language
        self.__min_trust_level = min_trust_level
        self.__debug_model = debug_model

        tesseract_dic_path = '{}/tessdata'.format(RESOURCES_PATH)
        tesseract_psm = '6'  # Assume a single uniform block of text.
        self.__tesseract_conf = '--tessdata-dir {} --psm {}'.format(tesseract_dic_path, tesseract_psm)

        self.neural_network = cv2.dnn.readNet(__EAST_DETECTOR_DATASET__)

    def convert_file_image_to_string(self, file, margin=0):
        self.__log_debug('start ocr from file {}'.format(file))
        img = self.__open_image_as_bgr(file)
        return self.convert_image_to_string(img, margin=margin)

    def convert_image_to_string(self, img, margin=0):
        img = self.__convert_image_perspective(img)

        img = self.__convert_image_to_gray(img)
        img = self.__filter_blur_gaussian(img)
        img = self.__filter_color_gaussian_adaptive_threshold(img)

        img = self.__erase_qrcode(img)
        img = self.__enlarge(img, 3)

        img = self.__filter_noise_dilate(img)
        for index in range(0, 100):
            img = self.__filter_noise_dilate(img)
            img = self.__filter_noise_erode(img)

        for index in range(0, 5):
            img = self.__filter_noise_erode(img)

        if margin > 0:
            img = self.__remove_margin(img, margin=margin)
        # self.__show_image(img, 'Fiscal ticket right to OCR')

        text = self.__convert_image_to_string(img)
        self.__log_debug(text)
        return text

    def __log_debug(self, message):
        if self.__debug_model:
            print(message)

    def __show_image(self, img, title='image'):
        if self.__debug_model:
            cv2.imshow(title, img)  # Show image
            cv2.setWindowProperty(title, cv2.WND_PROP_TOPMOST, 1)
            cv2.waitKey(0)  # wait for any press
            cv2.destroyAllWindows()  # Close window

    @staticmethod
    def __open_image_as_bgr(file):
        return cv2.imread(file)  # Open Image

    @staticmethod
    def __convert_image_to_gray(img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert image to gray

    @staticmethod
    def __invert_gray_color(gray):
        return __MAX_COLOR_VALUE__ - gray

    def __convert_image_to_canny_edge_to_qr(self, img):
        img = self.__convert_image_to_gray(img)
        img = self.__filter_color_gaussian_adaptive_threshold(img)
        for index in range(0, 30):
            img = self.__filter_noise_closure(img, 3)
        self.__show_image(img, 'filter')

        # for index in range(1, 70):
        #     self.__show_image(self.__filter_noise_erode(img, index), '{}'.format(index))

        for index in range(0, 25):
            img = self.__filter_noise_erode(img, 5)
            img = self.__filter_noise_dilate(img, 3)
            self.__show_image(img, '{}'.format(index))

        # for loop in range(0, 5):
        #
        #     for index in range(0, 5):
        #         img = self.__filter_noise_dilate(img, 3)
        #         self.__show_image(img, '{}-{}'.format(loop, index))

        return self.__filter_canny_edge(img)

    def __convert_image_to_canny_edge(self, img):
        img = self.__convert_image_to_gray(img)
        img = self.__filter_color_gaussian_adaptive_threshold(img)
        for index in range(0, 15):
            img = self.__filter_noise_erode(img, 4)
            img = self.__filter_noise_dilate(img, 3)
        return self.__filter_canny_edge(img)

    @staticmethod
    def __filter_color_binary_threshold(img, thresh=__MIN_COLOR_VALUE__, max_val=__MAX_COLOR_VALUE__):
        __, result = cv2.threshold(src=img, thresh=thresh, maxval=max_val, type=cv2.THRESH_BINARY)
        return result

    @staticmethod
    def __filter_color_otsu_threshold(img, thresh=__MIN_COLOR_VALUE__, max_val=__MAX_COLOR_VALUE__):
        __, result = cv2.threshold(src=img, thresh=thresh, maxval=max_val, type=cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        return result

    @staticmethod
    def __filter_color_mean_adaptive_threshold(img, block_size=11, subtracted=9):
        return cv2.adaptiveThreshold(src=img,
                                     maxValue=__MAX_COLOR_VALUE__,
                                     adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C,
                                     thresholdType=cv2.THRESH_BINARY,
                                     blockSize=block_size,
                                     C=subtracted)

    @staticmethod
    def __filter_color_gaussian_adaptive_threshold(img, block_size=11, subtracted=9):
        return cv2.adaptiveThreshold(src=img,
                                     maxValue=__MAX_COLOR_VALUE__,
                                     adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     thresholdType=cv2.THRESH_BINARY,
                                     blockSize=block_size,
                                     C=subtracted)

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
    def __filter_noise_erode(img, sensitivity=3):
        return cv2.erode(src=img, kernel=np.ones((sensitivity, sensitivity), np.uint8))

    @staticmethod
    def __filter_noise_dilate(img, sensitivity=3):
        return cv2.dilate(src=img, kernel=np.ones((sensitivity, sensitivity), np.uint8))

    @staticmethod
    def __filter_noise_opening(img, sensitivity=3):
        erode = FiscalTicketOcr.__filter_noise_erode(img, sensitivity)
        dilate = FiscalTicketOcr.__filter_noise_dilate(erode, sensitivity)
        return dilate

    @staticmethod
    def __filter_noise_closure(img, sensitivity=3):
        dilate = FiscalTicketOcr.__filter_noise_dilate(img, sensitivity)
        erode = FiscalTicketOcr.__filter_noise_erode(dilate, sensitivity)
        return erode

    @staticmethod
    def __filter_blur(img, size=5):
        return cv2.blur(img, (size, size))

    @staticmethod
    def __filter_blur_gaussian(img, size=5):
        return cv2.GaussianBlur(img, (size, size), 0)

    @staticmethod
    def __filter_blur_median(img, size=5):
        return cv2.medianBlur(img, size)

    @staticmethod
    def __filter_blur_bilateral(img):
        return cv2.bilateralFilter(img, 15, 40, 45)

    @staticmethod
    def __filter_canny_edge(img):
        return cv2.Canny(img, 40, 160)

    @staticmethod
    def __find_contours(img, sort_desc=True):
        contours = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        contours = sorted(contours, key=cv2.contourArea, reverse=sort_desc)[:6]
        return contours

    @staticmethod
    def __select_biggest_contour(contours):
        for contour, index in zip(contours, range(0, len(contours))):
            perimeter = cv2.arcLength(contour, True)
            sides = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            if len(sides) >= 4:
                return sides
        return None

    def __select_qr_contour(self, img, contours):
        for contour, index in zip(contours, range(0, len(contours))):
            perimeter = cv2.arcLength(contour, True)
            sides = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            print(len(sides), sides)

            if len(sides) >= 4:
                img = self.__draw_point(img, sides[0][0])
                img = self.__draw_point(img, sides[1][0])
                img = self.__draw_point(img, sides[2][0])
                img = self.__draw_point(img, sides[3][0])
                self.__show_image(img, '__sort_contour_points')
                return sides
        return None

    @staticmethod
    def __sort_contour_points(contour):
        points = contour.reshape((len(contour), 2))
        sorted_points = np.zeros((4, 1, 2), dtype=np.int32)

        add = points.sum(1)
        sorted_points[0] = points[np.argmin(add)]
        sorted_points[2] = points[np.argmax(add)]

        diff = np.diff(points, axis=1)
        sorted_points[1] = points[np.argmin(diff)]
        sorted_points[3] = points[np.argmax(diff)]
        return sorted_points

    def __erase_qrcode(self, img):
        invert = self.__invert_gray_color(img)

        invert = self.__filter_noise_closure(invert, 53)
        invert = self.__filter_noise_opening(invert, 21)

        contours = self.__find_contours(invert)
        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.06 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
            area = cv2.contourArea(c)
            ar = w / float(h)
            if len(approx) == 4 and area > 10000 and (ar > .85 and ar < 1.6) and w > 500 and h > 500:
                cv2.rectangle(img, (x, y), (x + w, y + h), __COLOR_WHITE_RGB__, cv2.FILLED)
        return img

    def __convert_image_perspective(self, img):
        img_edge = self.__convert_image_to_canny_edge(img)

        (height, wight) = img.shape[:2]

        contours = self.__find_contours(img_edge)

        fiscal_ticket_contour = self.__select_biggest_contour(contours)
        if fiscal_ticket_contour is not None:
            fiscal_ticket_contour = self.__sort_contour_points(fiscal_ticket_contour)

            pts1 = np.float32(fiscal_ticket_contour)
            pts2 = np.float32([[0, 0], [wight, 0], [wight, height], [0, height]])

            perspective_transform_matrix = cv2.getPerspectiveTransform(pts1, pts2)
            img = cv2.warpPerspective(img, perspective_transform_matrix, (wight, height))
        return img

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
