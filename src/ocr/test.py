import pytesseract
from src import RESOURCES_PATH
from src.ocr import __DEFAULT_LANGUAGE__
from src.ocr import image
from src.ocr import image_color_filter


if __name__ == '__main__':
    __language = __DEFAULT_LANGUAGE__

    tesseract_dic_path = '{}/tessdata'.format(RESOURCES_PATH)
    tesseract_psm = '6'  # Assume a single uniform block of text.
    __tesseract_conf = '--tessdata-dir {} --psm {}'.format(tesseract_dic_path, tesseract_psm)

    img = image.open_image_as_bgr('{}/images/parts/part_5.png'.format(RESOURCES_PATH))
    img = image_color_filter.image_to_gray(img)
    img = image.reduce(img, 0.5)

    image .show_image(img, 'Image right to Ocr')

    text = pytesseract.image_to_string(img, lang=__language, config=__tesseract_conf)
    print(text)
