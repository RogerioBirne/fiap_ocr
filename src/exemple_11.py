from src import RESOURCES_PATH
from ocr.fiscal_ticket_ocr import FiscalTicketOcr
from ocr.fiscal_ticket_pnl import FiscalTicketPnl
import textdistance


if __name__ == '__main__':
    fiscal_ticket_ocr = FiscalTicketOcr(debug_model=True)
    fiscal_ticket_pnl = FiscalTicketPnl()
    fiscal_ticket = fiscal_ticket_ocr.convert_file_image_to_string('{}/images/example_11.jpg'.format(RESOURCES_PATH))

    with open('{}/images/example_11.txt'.format(RESOURCES_PATH), 'r') as file:
        digit_text = file.read()
        normalized_similarity = textdistance.hamming.normalized_similarity(digit_text, fiscal_ticket)
        print('normalized_similarity', normalized_similarity)
