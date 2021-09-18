from src import RESOURCES_PATH
from ocr.fiscal_ticket_ocr import FiscalTicketOcr
from ocr.fiscal_ticket_pnl import FiscalTicketPnl

if __name__ == '__main__':
    fiscal_ticket_ocr = FiscalTicketOcr(debug_model=True)
    fiscal_ticket_pnl = FiscalTicketPnl()
    fiscal_ticket = fiscal_ticket_ocr.convert_file_image_to_string('{}/images/example_01.jpg'.format(RESOURCES_PATH))
    # fiscal_ticket = fiscal_ticket_ocr.convert_file_image_to_string('{}/images/example_02.jpg'.format(RESOURCES_PATH))
    # fiscal_ticket = fiscal_ticket_ocr.convert_file_image_to_string('{}/images/example_03.png'.format(RESOURCES_PATH))
    # fiscal_ticket = fiscal_ticket_ocr.convert_file_image_to_string('{}/images/example_04.jpg'.format(RESOURCES_PATH))
    # fiscal_ticket = fiscal_ticket_ocr.convert_file_image_to_string('{}/images/example_05.jpg'.format(RESOURCES_PATH))
    # fiscal_ticket = fiscal_ticket_ocr.convert_file_image_to_string('{}/images/example_06.jpg'.format(RESOURCES_PATH))
    # fiscal_ticket = fiscal_ticket_ocr.convert_file_image_to_string('{}/images/example_07.jpg'.format(RESOURCES_PATH))
    # fiscal_ticket = fiscal_ticket_ocr.convert_file_image_to_string('{}/images/example_08.jpg'.format(RESOURCES_PATH))
    # fiscal_ticket = fiscal_ticket_ocr.convert_file_image_to_string('{}/images/example_09.jpg'.format(RESOURCES_PATH))
    print(fiscal_ticket_pnl.extract_data(fiscal_ticket))
