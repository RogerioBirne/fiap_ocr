from src.tesseract.tesseract_functions import *
from src import RESOURCES_PATH


def tesseract_example():
    img = cv2.imread(RESOURCES_PATH + '/Imagens/receita01.jpg')  # Open Image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert image to gray
    val, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    results = pytesseract.image_to_data(otsu, lang='eng', config=TESSERACT_CONF, output_type=Output.DICT)

    print_ocr_on_image(otsu, results)


if __name__ == '__main__':
    tesseract_example()