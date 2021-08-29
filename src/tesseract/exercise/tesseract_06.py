import pytesseract
import numpy as np
import cv2
from pytesseract import Output
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import pprint
import re


def tesseract_example():
    font = '../../../resources/Fontes/calibri.ttf'

    img = cv2.imread('../../../resources/Imagens/tabela_teste.jpg')  # Open Image
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert image to rgb

    config = '--tessdata-dir ../../../resources/tessdata'  # Config with language portuguese
    results = pytesseract.image_to_data(rgb, lang='por', config=config, output_type=Output.DICT)  # Convert Image to Text from portuguese

    pretty = pprint.PrettyPrinter(width=200)
    pretty.pprint(results)

    min_conf = 40
    date_pattern = '^(((0[1-9]|[12][0-9]|3[01])[- /.](0[13578]|1[02])|(0[1-9]|[12][0-9]|30)[- /.](0[469]|11)|(0[1-9]|1\d|2[0-8])[- /.]02)[- /.]\d{4}|29[- /.]02[- /.](\d{2}(0[48]|[2468][048]|[13579][26])|([02468][048]|[1359][26])00))$'

    rgb_copy = rgb.copy()
    for index in range(0, len(results['text'])):
        conf = results['conf'][index]

        if int(conf) > min_conf:
            x, y, text, rgb_copy = text_box(results, rgb_copy, index)
            if re.match(date_pattern, text):
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
