from src import RESOURCES_PATH
from ocr import fiscal_ticket_ocr
from ocr.fiscal_ticket_pnl import FiscalTicketPnl
import textdistance

if __name__ == '__main__':
    fiscal_ticket_pnl = FiscalTicketPnl()
    fiscal_ticket = fiscal_ticket_ocr.convert_file_image_to_string(
        '{}/images/example_11.jpg'.format(RESOURCES_PATH)).replace('\n', '')

    with open('{}/images/example_11.txt'.format(RESOURCES_PATH), 'r') as file:
        digit_text = file.read().replace('\n', '')

        distance = textdistance.hamming.distance(fiscal_ticket, digit_text)
        print('distance', distance)

        normalized_similarity = textdistance.hamming.normalized_similarity(fiscal_ticket, digit_text)
        print('normalized_similarity', normalized_similarity)
