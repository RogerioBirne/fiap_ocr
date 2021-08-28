import pytesseract
import numpy as np
import cv2
from pytesseract import Output
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import pprint


def tesseract_example():
    font = 'resources/Fontes/calibri.ttf'

    img = cv2.imread('resources/Imagens/img-process.jpg')  # Open Image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert image to gray

    config = '--tessdata-dir resources/tessdata'  # Config with language portuguese
    results = pytesseract.image_to_data(gray, lang='eng', config=config, output_type=Output.DICT)

    pretty = pprint.PrettyPrinter(width=200)
    pretty.pprint(results)

    min_conf = 90

    rgb_copy = gray.copy()
    for index in range(0, len(results['text'])):
        conf = results['conf'][index]

        if int(conf) > min_conf:
            x, y, text, rgb_copy = text_box(results, rgb_copy, index)
            rgb_copy = write_text(text, x, y, rgb_copy, font, font_length=12)

    cv2.imshow('displaymywindows', rgb_copy)  # Show image
    cv2.setWindowProperty('displaymywindows', cv2.WND_PROP_TOPMOST, 1)
    cv2.waitKey(0)  # wait for any press
    cv2.destroyAllWindows()  # Close window


def text_box(result, img, index, color=(255, 100, 0)):
    x = result['left'][index]
    y = result['top'][index]
    w = result['width'][index]
    h = result['height'][index]
    text = result['text'][index]

    cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)

    return x, y, text, img


def write_text(text, x, y, img, font, font_length=32):
    image_font = ImageFont.truetype(font, font_length)
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    draw.text((x, y - font_length), text, font=image_font)
    return np.array(img_pil)


if __name__ == '__main__':
    tesseract_example()
