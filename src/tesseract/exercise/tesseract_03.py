import pytesseract
import cv2


def tesseract_example():
    img = cv2.imread('../../../resources/Imagens/trecho-livro.jpg')  # Open Image
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert image to rgb

    cv2.imshow('displaymywindows', rgb)  # Show image
    cv2.waitKey(0)  # wait for any press
    cv2.destroyAllWindows()  # Close window

    config = '--tessdata-dir ../../../resources/tessdata --psm 6'  # Config with language portuguese
    text = pytesseract.image_to_string(rgb, lang='por', config=config)  # Convert Image to Text from portuguese
    print(text)  # Print result


if __name__ == '__main__':
    tesseract_example()
