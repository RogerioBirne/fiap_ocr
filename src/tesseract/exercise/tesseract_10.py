import pytesseract
from pytesseract import Output
from src.tesseract.utils.utils import *


def tesseract_example():
    img = cv2.imread('../../../resources/Imagens/livro02.jpg')  # Open Image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert image to gray

    adapt_media = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 9)

    results = pytesseract.image_to_data(adapt_media, lang='por', config=TESSERACT_CONF, output_type=Output.DICT)

    print_ocr_on_image(adapt_media, results)


if __name__ == '__main__':
    tesseract_example()
