from src.tesseract.tesseract_functions import *
from imutils.object_detection import non_max_suppression


def tesseract_example():
    detector = '../../../resources/Modelos/frozen_east_text_detection.pb'
    wight, height = 320, 320

    img = read_file_as_bgr('../../../resources/Imagens/caneca.jpg')
    min_conf = 0.9

    img_wight, img_height, __ = img.shape
    proportion_wight = img_wight / float(wight)
    proportion_height = img_height / float(height)

    print(img_wight, img_height)
    print(proportion_wight, proportion_height)
    img = resize(img, wight, height)

    show_image(img)
    # img = convert_image_to_gray(img)
    # img = filter_color_otsu_threshold(img)
    # img = invert_gray_color(img)
    #
    # results = convert_image_to_data(img, 'por')
    # print_ocr_on_image(img, results)


if __name__ == '__main__':
    tesseract_example()
