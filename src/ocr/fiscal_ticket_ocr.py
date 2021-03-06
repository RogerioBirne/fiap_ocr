import pytesseract
from pytesseract import Output
from src import RESOURCES_PATH
from src.ocr import __DEFAULT_LANGUAGE__, __DEFAULT_DEBUG__
from src.ocr import image
from src.ocr import image_blur
from src.ocr import image_noise_filter
from src.ocr import image_color_filter
from src.ocr import fiscal_ticket_extractor
from src.ocr import image_qr_code_eraser
from src.ocr import image_bar_code_eraser
from src.ocr import fiscal_ticket_text_filter

# This script can transform a fiscal ticket image in text using tesseract and opencv
__TESSERACT_DIC_PATH__ = '{}/tessdata'.format(RESOURCES_PATH)
__TESSERACT_PSM__ = '6'  # Assume a single uniform block of text.
__TESSERACT_CONF__ = '--tessdata-dir {} --psm {}'.format(__TESSERACT_DIC_PATH__, __TESSERACT_PSM__)


def convert_file_image_to_string(file, margin=0, language=__DEFAULT_LANGUAGE__, config=__TESSERACT_CONF__,
                                 debug=__DEFAULT_DEBUG__):
    img = image.open_image_as_bgr(file)
    return convert_image_to_string(img, margin=margin, language=language, config=config, debug=debug)


def convert_image_to_string(img, margin=0, language=__DEFAULT_LANGUAGE__, config=__TESSERACT_CONF__,
                            debug=__DEFAULT_DEBUG__):
    img = __extract_fiscal_ticket_to_ocr(img, margin=margin)
    if debug is True:
        image.show_image(img, 'Image right to Ocr')

    text = __convert_image_to_string_by_tesseract(img, language=language, config=config)
    text = fiscal_ticket_text_filter.filter_text(text)
    if debug is True:
        print(text)
    return text


def __extract_fiscal_ticket_to_ocr(img, margin=0):
    img = fiscal_ticket_extractor.convert_image_perspective(img)

    img = image_color_filter.image_to_gray(img)
    img = image_color_filter.color_gaussian_adaptive_threshold(img)

    img = image_qr_code_eraser.erase_qrcode(img, margin=10)
    img = image_bar_code_eraser.erase_barcode(img)

    height = img.shape[0]
    if height > 3000:
        for __ in range(5):
            img = image_noise_filter.noise_opening(img, 7)
            img = image_blur.blur(img)
        img = image_noise_filter.noise_erode(img)
    else:
        img = image_blur.blur(img)

    if margin > 0:
        img = image.remove_margin(img, margin=margin)

    return img


def __convert_image_to_string_by_easy(img, language=__DEFAULT_LANGUAGE__):
    languages = ['en']
    if language == 'por':
        languages.append('pt')
    elif language != 'en':
        languages.append(language)

    reader = easyocr.Reader(languages)
    result = reader.readtext(img)
    return ' '.join(text for (pts, text, level) in result if level > 0.1).upper()


def __convert_image_to_string_by_tesseract(img, language=__DEFAULT_LANGUAGE__, config=__TESSERACT_CONF__):
    return pytesseract.image_to_string(img, lang=language, config=config).upper()


def __convert_image_to_string_by_tesseract_with_conf(img, min_conf, language=__DEFAULT_LANGUAGE__,
                                                     config=__TESSERACT_CONF__):
    data = pytesseract.image_to_data(img, lang=language, config=config, output_type=Output.DICT)
    return ' '.join(text for (conf, text) in zip(data['conf'], data['text']) if int(conf) > min_conf).upper()
