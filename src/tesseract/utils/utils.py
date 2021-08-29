import numpy as np
import cv2
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import pprint
import pytesseract
from pytesseract import Output

WINDOW_NAME = 'displaymywindows'
CALIBRI_FONT = '../../../resources/Fontes/calibri.ttf'
MIN_CONF = 90
TESSERACT_CONF = '--tessdata-dir ../../../resources/tessdata'  # Config with language portuguese


def read_file_as_bgr(file):
    return cv2.imread(file)  # Open Image


def convert_image_to_gray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert image to gray


def invert_gray_color(gray):
    return 255 - gray


def filter_binary_threshold(img, min=0, max=255):
    __, result = cv2.threshold(img, min, max, cv2.THRESH_BINARY)
    return result


def filter_otsu_threshold(img, min=0, max=255):
    __, result = cv2.threshold(img, min, max, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return result


def filter_mean_adaptive_threshold(img, block_size=11, subtracted=9):
    return cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, subtracted)


def filter_gaussian_adaptive_threshold(img, block_size=11, subtracted=9):
    return cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, subtracted)




def convert_image_to_data(img):
    return pytesseract.image_to_data(img, lang='por', config=TESSERACT_CONF, output_type=Output.DICT)


def print_ocr_on_image(img, results):
    pretty_print_dict(results)

    img_copy = img.copy()
    for index in range(0, len(results['text'])):
        conf = results['conf'][index]

        if int(conf) > MIN_CONF:
            x, y, text, img_copy = text_box(results, img_copy, index)
            img_copy = write_text(text, x, y, img_copy, CALIBRI_FONT, font_length=12)

    show_image(img_copy)


def show_image(img):
    cv2.imshow(WINDOW_NAME, img)  # Show image
    cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_TOPMOST, 1)
    cv2.waitKey(0)  # wait for any press
    cv2.destroyAllWindows()  # Close window


def pretty_print_dict(value):
    pretty = pprint.PrettyPrinter(width=200)
    pretty.pprint(value)


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
