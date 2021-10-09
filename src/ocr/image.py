import numpy as np
import cv2
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from src.ocr import __COLOR_RED_RGB__, __COLOR_GREEN_RGB__, __COLOR_BLUE_RGB__, __COLOR_BLACK_RGB__, __COLOR_WHITE_RGB__


# This class can work with images
class Image:
    @staticmethod
    def show_image(img, title='image'):
        cv2.imshow(title, img)  # Show image
        cv2.setWindowProperty(title, cv2.WND_PROP_TOPMOST, 1)
        cv2.waitKey(0)  # wait for any press
        cv2.destroyAllWindows()  # Close window

    @staticmethod
    def open_image_as_bgr(file):
        return cv2.imread(file)  # Open Image

    @staticmethod
    def resize(img, height, wight):
        return cv2.resize(src=img, dsize=(height, wight))

    @staticmethod
    def enlarge(img, factor):
        return cv2.resize(src=img, dsize=None, fx=factor, fy=factor, interpolation=cv2.INTER_CUBIC)

    @staticmethod
    def reduce(img, factor):
        return cv2.resize(src=img, dsize=None, fx=factor, fy=factor, interpolation=cv2.INTER_AREA)

    @staticmethod
    def remove_margin(img, margin=20):
        (height, wight) = img.shape[:2]
        return img[margin:height - margin, margin:wight - margin]

    @staticmethod
    def draw_point(img, point, color=__COLOR_RED_RGB__):
        return cv2.circle(img, point, radius=0, color=color, thickness=20)

    @staticmethod
    def draw_box(img, point_1, point_2, color=__COLOR_RED_RGB__, border_size=2):
        return cv2.rectangle(img, pt1=point_1, pt2=point_2, color=color, thickness=border_size)

    @staticmethod
    def write_text(text, img, x, y, font, font_length=32):
        image_font = ImageFont.truetype(font, font_length)
        img_pil = Image.fromarray(img)
        draw = ImageDraw.Draw(img_pil)
        draw.text((x, y - font_length), text, font=image_font)
        return np.array(img_pil)
