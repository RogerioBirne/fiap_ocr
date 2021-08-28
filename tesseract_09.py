import pytesseract
from pytesseract import Output
from utils import *


def tesseract_example():
    img = cv2.imread('resources/Imagens/receita01.jpg')  # Open Image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert image to gray
    val, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    results = pytesseract.image_to_data(otsu, lang='eng', config=TESSERACT_CONF, output_type=Output.DICT)

    pretty_print_dict(results)

    rgb_copy = otsu.copy()
    for index in range(0, len(results['text'])):
        conf = results['conf'][index]

        if int(conf) > MIN_CONF:
            x, y, text, rgb_copy = text_box(results, rgb_copy, index)
            rgb_copy = write_text(text, x, y, rgb_copy, CALIBRI_FONT, font_length=12)

    show_image(rgb_copy)


if __name__ == '__main__':
    tesseract_example()
