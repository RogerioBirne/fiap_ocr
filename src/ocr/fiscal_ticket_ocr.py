import numpy as np
import cv2
import pytesseract
from pytesseract import Output
import imutils
from imutils.object_detection import non_max_suppression
from src import RESOURCES_PATH

__DEFAULT_LANGUAGE__ = 'por'
__DEFAULT_DEBUG__ = False
__DEFAULT_MIN_TRUST_LEVEL__ = 0.9
__MIN_COLOR_VALUE__ = 0
__MAX_COLOR_VALUE__ = 255

__EAST_OVERLAP_THRESH__ = 0.5
__EAST_LAYER_NAMES__ = ['feature_fusion/Conv_7/Sigmoid', 'feature_fusion/concat_3']
__EAST_BASE_SIZE__ = 32
__EAST_ENLARGE_FACTOR__ = 3


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

        self.__east_detector_dataset = '{}/model/frozen_east_text_detection.pb'.format(RESOURCES_PATH)
        self.neural_network = cv2.dnn.readNet(self.__east_detector_dataset)

    def convert_file_image_to_string(self, file, margin=0):
        self.__log_debug('start ocr from file {}'.format(file))
        img = self.__open_image_as_bgr(file)
        return self.convert_image_to_string(img, margin=margin)

    def convert_image_to_string(self, img, margin=0):
        # self.__show_image(img, 'Original image')

        img = self.__convert_image_perspective(img)
        self.__show_image(img, 'After fix perspective')

        img = self.__enlarge(img, 2)
        img = self.__convert_image_to_gray(img)
        img = self.__filter_blur_gaussian(img)
        img = self.__filter_color_otsu_threshold(img)
        if margin > 0:
            img = self.__remove_margin(img, margin=margin)
        self.__show_image(img, 'Fiscal ticket right to OCR')

        text = self.__convert_image_to_string(img)
        self.__log_debug(text)
        return text

    def __log_debug(self, message):
        if self.__debug_model:
            print(message)

    def __show_image(self, img, title):
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

    def __convert_image_to_canny_edge(self, img):
        img = self.__convert_image_to_gray(img)
        img = self.__filter_blur_gaussian(img)
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
        return cv2.Canny(img, 60, 160)

    @staticmethod
    def __find_contours(img, sort_desc=True):
        contours = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        contours = sorted(contours, key=cv2.contourArea, reverse=sort_desc)[:6]
        return contours

    @staticmethod
    def __select_biggest_contour(contours):
        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            sides = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            if len(sides) == 4:
                return sides
        return None

    @staticmethod
    def __sort_contour_points(contour):
        points = contour.reshape((4, 2))
        sorted_points = np.zeros((4, 1, 2), dtype=np.int32)

        add = points.sum(1)
        sorted_points[0] = points[np.argmin(add)]
        sorted_points[2] = points[np.argmax(add)]

        diff = np.diff(points, axis=1)
        sorted_points[1] = points[np.argmin(diff)]
        sorted_points[3] = points[np.argmax(diff)]

        return sorted_points

    def __convert_image_perspective(self, img):
        img_result = self.__convert_image_perspective_by_contours(img)

        # detections = self.__image_to_detections(img_result)
        # if len(detections) < 10:
        #     detections = self.__image_to_detections(img)
        #     img_result = self.__detections_to_roi(img, detections)
        #     image_osd = pytesseract.image_to_osd(img)
        #     print(image_osd)
        #     exit(0)
        #     #TODO: buscar uma forma otimizada para selecionar o maior roi

        return img_result

    def __convert_image_perspective_by_contours(self, img):
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

    def __image_to_detections(self, img, overlap_thresh=__EAST_OVERLAP_THRESH__):
        img = self.__enlarge(img, __EAST_ENLARGE_FACTOR__)
        img = self.__convert_image_to_gray(img)
        img = self.__filter_color_otsu_threshold(img)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)  # Convert image to gray

        img_height, img_wight = img.shape[:2]
        pad_height = ((int(img_height / __EAST_BASE_SIZE__) + 1) * __EAST_BASE_SIZE__) - img_height
        pad_wight = ((int(img_wight / __EAST_BASE_SIZE__) + 1) * __EAST_BASE_SIZE__) - img_wight
        img = cv2.copyMakeBorder(img, 0, pad_height, 0, pad_wight, cv2.BORDER_CONSTANT, value=[255, 255, 255])

        img_height, img_wight = img.shape[:2]
        img_blob = cv2.dnn.blobFromImage(img, 1.0, (img_wight, img_height), swapRB=True, crop=False)

        self.neural_network.setInput(img_blob)

        scores_map, geometries = self.neural_network.forward(__EAST_LAYER_NAMES__)
        lines, columns = scores_map.shape[2:4]

        boxes = []
        trusts = []

        for line in range(0, lines):
            scores = scores_map[0, 0, line]
            for column in range(0, columns):
                if scores[column] >= self.__min_trust_level:
                    angles, x_data_0, x_data_1, x_data_2, x_data_3 = self.__geometric_data(geometries, line)
                    start_x, start_y, end_x, end_y = self.__geometric_calc(line, column, angles, x_data_0, x_data_1,
                                                                           x_data_2, x_data_3)

                    trusts.append(scores[column])
                    boxes.append((start_x, start_y, end_x, end_y))

        detections = non_max_suppression(np.array(boxes), probs=trusts, overlapThresh=overlap_thresh)
        self.__log_debug('east detections: {}'.format(len(detections)))

        return [(int(start_x / __EAST_ENLARGE_FACTOR__),
                 int(start_y / __EAST_ENLARGE_FACTOR__),
                 int(end_x / __EAST_ENLARGE_FACTOR__),
                 int(end_y / __EAST_ENLARGE_FACTOR__))
                for (start_x, start_y, end_x, end_y) in detections]

    @staticmethod
    def __detections_to_roi(img, detections, margin=5):
        arr = np.array(detections)

        img_height, img_wight = img.shape[:2]

        min_start_x = min(arr[:, 0])
        min_start_y = min(arr[:, 1])
        max_end_x = max(arr[:, 2])
        max_end_y = max(arr[:, 3])

        min_start_x = max(0, min_start_x - margin)
        min_start_y = max(0, min_start_y - margin)
        max_end_x = min(img_wight, max_end_x + margin)
        max_end_y = min(img_height, max_end_y + margin)

        return img[min_start_y:max_end_y, min_start_x:max_end_x]

    @staticmethod
    def __geometric_data(geometry, y):
        x_data_0 = geometry[0, 0, y]
        x_data_1 = geometry[0, 1, y]
        x_data_2 = geometry[0, 2, y]
        x_data_3 = geometry[0, 3, y]
        angles = geometry[0, 4, y]
        return angles, x_data_0, x_data_1, x_data_2, x_data_3

    @staticmethod
    def __geometric_calc(line, column, angles, x_data_0, x_data_1, x_data_2, x_data_3):
        (offset_x, offset_y) = (column * 4.0, line * 4.0)
        angle = angles[column]
        cos = np.cos(angle)
        sin = np.sin(angle)
        height = x_data_0[column] + x_data_2[column]
        wight = x_data_1[column] + x_data_3[column]

        end_x = int(offset_x + (cos * x_data_1[column]) + (sin * x_data_2[column]))
        end_y = int(offset_y - (sin * x_data_1[column]) + (cos * x_data_2[column]))

        start_x = int(end_x - wight)
        start_y = int(end_y - height)

        return start_x, start_y, end_x, end_y

    def __convert_image_to_string(self, img):
        return pytesseract.image_to_string(img,
                                           lang=self.__language,
                                           config=self.__tesseract_conf)

    def __convert_image_to_data(self, img):
        return pytesseract.image_to_data(img,
                                         lang=self.__language,
                                         config=self.__tesseract_conf,
                                         output_type=Output.DICT)
