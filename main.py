import pytesseract
import numpy as np
import cv2


def tesseract_example():
    img = cv2.imread('resources/Imagens/teste02.jpg')

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    text = pytesseract.image_to_string(rgb)

    print(text)

    # cv2.imshow('displaymywindows', rgb)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


if __name__ == '__main__':
    tesseract_example()
