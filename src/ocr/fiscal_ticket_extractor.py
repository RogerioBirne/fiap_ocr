import numpy as np
import cv2
import math
from PIL import Image
from src.ocr.image import Image
from src.ocr.image_color_filter import ImageColorFilter
from src.ocr.image_contour_filter import ImageContourFilter


# This class can extract a fiscal_ticket inside image
class FiscalTicketExtractor:
    @staticmethod
    def convert_image_perspective(img):
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
            img = FiscalTicketExtractor.__fix_image_ratio(img, ratio_src, fiscal_ticket_contour)
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
        return Image.resize(img, height, int((height // ratio_src) * perspective_factor))

