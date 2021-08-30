import pytesseract
import cv2
from src import RESOURCES_PATH


def tesseract_example():
    img = cv2.imread(RESOURCES_PATH + '/Imagens/teste02.jpg')  # Open Image
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert image to rgb

    # cv2.imshow('displaymywindows', rgb)  # Show image
    # cv2.waitKey(0)  # wait for any press
    # cv2.destroyAllWindows()  # Close window

    config = '--tessdata-dir {}/tessdata'.format(RESOURCES_PATH)  # Config with language portuguese
    text = pytesseract.image_to_string(rgb, lang='por', config=config)  # Convert Image to Text from portuguese
    print(text)  # Print result


if __name__ == '__main__':
    tesseract_example()
