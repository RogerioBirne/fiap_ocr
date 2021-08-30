from src.tesseract.tesseract_functions import *
from imutils.object_detection import non_max_suppression
from src import RESOURCES_PATH

_EAST_MIN_CONF = 0.9
_EAST_LAYER_NAMES = ['feature_fusion/Conv_7/Sigmoid', 'feature_fusion/concat_3']
_EAST_DETECTOR_DATASET = RESOURCES_PATH + '/Modelos/frozen_east_text_detection.pb'
_EAST_BASE_HEIGHT, _EAST_BASE_WIGHT = 2560, 2560


def image_to_detections(img, min_conf=_EAST_MIN_CONF):
    img_height, img_wight, __ = img.shape

    proportion_height = img_height / float(_EAST_BASE_HEIGHT)
    proportion_wight = img_wight / float(_EAST_BASE_WIGHT)

    img_resized = resize(img, _EAST_BASE_HEIGHT, _EAST_BASE_WIGHT)

    neural_network = cv2.dnn.readNet(_EAST_DETECTOR_DATASET)

    img_blob = cv2.dnn.blobFromImage(img_resized, 1.0, (_EAST_BASE_WIGHT, _EAST_BASE_HEIGHT), swapRB=True, crop=False)

    neural_network.setInput(img_blob)

    scores_map, geometries = neural_network.forward(_EAST_LAYER_NAMES)
    lines, columns = scores_map.shape[2:4]

    boxes = []
    trusts = []

    for line in range(0, lines):
        scores = scores_map[0, 0, line]
        for column in range(0, columns):
            if scores[column] >= min_conf:
                angles, x_data_0, x_data_1, x_data_2, x_data_3 = geometric_data(geometries, line)
                start_x, start_y, end_x, end_y = geometric_calc(line, column, angles, x_data_0, x_data_1, x_data_2, x_data_3)

                trusts.append(scores[column])
                boxes.append((start_x, start_y, end_x, end_y))

    detections = non_max_suppression(np.array(boxes), probs=trusts)
    return [(int(start_x * proportion_wight),
             int(start_y * proportion_height),
             int(end_x * proportion_wight),
             int(end_y * proportion_height))
            for (start_x, start_y, end_x, end_y) in detections]


def detections_to_roi_list(img, detections, margin=5):
    img_copy = img.copy()
    return [img_copy[start_y - margin:end_y + margin, start_x + margin:end_x + margin] for (start_x, start_y, end_x, end_y) in detections]


def geometric_data(geometry, y):
    x_data_0 = geometry[0, 0, y]
    x_data_1 = geometry[0, 1, y]
    x_data_2 = geometry[0, 2, y]
    x_data_3 = geometry[0, 3, y]
    angles = geometry[0, 4, y]
    return angles, x_data_0, x_data_1, x_data_2, x_data_3


def geometric_calc(line, column, angles, x_data_0, x_data_1, x_data_2, x_data_3):
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
