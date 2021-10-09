import pytesseract
from pytesseract import Output
from src import RESOURCES_PATH
from src.ocr import __DEFAULT_LANGUAGE__
from src.ocr.image import Image
from src.ocr.image_blur import ImageBlur
from src.ocr.image_noise_filter import ImageNoiseFilter
from src.ocr.image_color_filter import ImageColorFilter
from src.ocr.fiscal_ticket_extractor import FiscalTicketExtractor
from src.ocr.image_qr_code_eraser import ImageQrCodeEraser


# This class can transform a fiscal ticket image in text using tesseract and opencv
class FiscalTicketOcr:

    def __init__(self, language=__DEFAULT_LANGUAGE__):
        self.__language = language

        tesseract_dic_path = '{}/tessdata'.format(RESOURCES_PATH)
        tesseract_psm = '6'  # Assume a single uniform block of text.
        self.__tesseract_conf = '--tessdata-dir {} --psm {}'.format(tesseract_dic_path, tesseract_psm)

    def convert_file_image_to_string(self, file, margin=0):
        img = Image.open_image_as_bgr(file)
        return self.convert_image_to_string(img, margin=margin)

    def convert_image_to_string(self, img, margin=0):
        img = FiscalTicketOcr.__extract_fiscal_ticket_to_ocr(img, margin=margin)

        text = self.__convert_image_to_string(img)
        print(text)
        return text

    @staticmethod
    def __extract_fiscal_ticket_to_ocr(img, margin=0):
        img = FiscalTicketExtractor.convert_image_perspective(img)

        img = ImageColorFilter.image_to_gray(img)
        img = ImageColorFilter.color_gaussian_adaptive_threshold(img)

        img = ImageQrCodeEraser.erase_qrcode(img, margin=25)

        img = ImageNoiseFilter.noise_closure(img)
        img = ImageNoiseFilter.noise_erode(img)

        if margin > 0:
            img = Image.remove_margin(img, margin=margin)
        return img

    def __convert_image_to_string(self, img):
        return pytesseract.image_to_string(img,
                                           lang=self.__language,
                                           config=self.__tesseract_conf)

    def __convert_image_to_data(self, img):
        return pytesseract.image_to_data(img,
                                         lang=self.__language,
                                         config=self.__tesseract_conf,
                                         output_type=Output.DICT)
