from src.tesseract.tesseract_functions import *
from src.east.east_functions import *
from src import RESOURCES_PATH


def tesseract_ocr():
    img = read_file_as_bgr(RESOURCES_PATH + '/Imagens/fiscal_docs/example_2.png')
    img = convert_image_to_gray(img)
    img = filter_color_gaussian_adaptive_threshold(img)

    results = convert_image_to_data(img, 'por')
    print_ocr_on_image(img, results)


def east_ocr():
    img = read_file_as_bgr(RESOURCES_PATH + '/Imagens/fiscal_docs/example_2.png')

    detections = image_to_detections(img)

    roi_list = detections_to_roi_list(img, detections)
    results = ''

    img_copy = img.copy()
    for index in range(0, len(roi_list)):
        roi = roi_list[index]
        detection = detections[index]

        if min(roi.shape[:2]) > 0:
            # roi = convert_image_to_gray(roi)
            # roi = filter_color_otsu_threshold(roi)

            cv2.rectangle(img_copy, (detection[0], detection[1]), (detection[2], detection[3]), (0, 255, 0), 1)

            # results += convert_image_to_string(roi, 'por')['text']

    # print(results)
    show_image(img_copy)


if __name__ == '__main__':
    east_ocr()
