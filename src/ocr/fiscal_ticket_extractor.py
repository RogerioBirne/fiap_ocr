import numpy as np
import cv2
import math
from src.ocr import image
from src.ocr import image_color_filter
from src.ocr import image_contour_filter


# This script can extract a fiscal_ticket inside image
def convert_image_perspective(img):
    img_edge = image_color_filter.image_to_canny_edge(img)

    (height, wight) = img.shape[:2]
    ratio_src = height / wight

    contours = image_contour_filter.find_contours(img_edge)

    fiscal_ticket_contour = image_contour_filter.select_biggest_contour(contours)
    if fiscal_ticket_contour is not None:
        fiscal_ticket_contour = image_contour_filter.sort_contour_points(fiscal_ticket_contour)
        pts1 = np.float32(fiscal_ticket_contour)
        pts2 = np.float32([[0, 0], [wight, 0], [wight, height], [0, height]])

        perspective_transform_matrix = cv2.getPerspectiveTransform(pts1, pts2)
        img = cv2.warpPerspective(img, perspective_transform_matrix, (wight, height))
        img = __fix_image_ratio(img, ratio_src, fiscal_ticket_contour)
    return img


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

    height = img.shape[0]
    return image.resize(img, height, int((height // ratio_src) * perspective_factor))
