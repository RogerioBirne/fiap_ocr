import numpy as np
import cv2
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import pprint

WINDOW_NAME = 'displaymywindows'
CALIBRI_FONT = 'resources/Fontes/calibri.ttf'
MIN_CONF = 90
TESSERACT_CONF = '--tessdata-dir resources/tessdata'  # Config with language portuguese

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
