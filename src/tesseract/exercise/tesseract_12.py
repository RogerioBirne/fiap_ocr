from src.tesseract.tesseract_functions import *


def tesseract_example():
    img = read_file_as_bgr('../../../resources/Imagens/texto-opencv2.jpg')
    img = convert_image_to_gray(img)
    img = filter_noise_closure(img, 5)
    img = invert_gray_color(img)

    results = convert_image_to_data(img, 'eng')
    print_ocr_on_image(img, results)


if __name__ == '__main__':
    tesseract_example()
