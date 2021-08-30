from src.tesseract.tesseract_functions import *
from src import RESOURCES_PATH


def tesseract_example():
    img = read_file_as_bgr(RESOURCES_PATH + '/Imagens/frase.jpg')
    img = convert_image_to_gray(img)
    img = filter_color_otsu_threshold(img)
    img = invert_gray_color(img)

    results = convert_image_to_data(img, 'por')
    print_ocr_on_image(img, results)


if __name__ == '__main__':
    tesseract_example()
