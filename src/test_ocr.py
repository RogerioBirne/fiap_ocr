from src import RESOURCES_PATH
from src.ocr import fiscal_ticket_ocr
import textdistance


def debug_ocr_with_accuracy(image_filename, text_filename, debug=True):
    print('start scan')
    fiscal_ticket = fiscal_ticket_ocr.convert_file_image_to_string(
        '{}/images/{}'.format(RESOURCES_PATH, image_filename), debug=debug)

    with open('{}/images/{}'.format(RESOURCES_PATH, text_filename), 'r') as file:
        digit_text = file.read()
        print('scanned image: [{}] and compare to: [{}]'.format(image_filename, text_filename))

        distance = textdistance.damerau_levenshtein.distance(digit_text, fiscal_ticket)
        print('distance', distance)

        normalized_similarity = textdistance.damerau_levenshtein.normalized_similarity(digit_text, fiscal_ticket)
        print('normalized_similarity', normalized_similarity)
    print('--------------------------------------------------')
