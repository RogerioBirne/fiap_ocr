from src import test_ocr

if __name__ == '__main__':
    fiscal_ticket = test_ocr.debug_ocr_with_accuracy('example_01.jpg', 'example_01.txt')
    fiscal_ticket = test_ocr.debug_ocr_with_accuracy('example_02.jpg', 'example_02.txt')
    fiscal_ticket = test_ocr.debug_ocr_with_accuracy('example_03.jpg', 'example_03.txt')
    fiscal_ticket = test_ocr.debug_ocr_with_accuracy('example_04.jpg', 'example_04.txt')
    fiscal_ticket = test_ocr.debug_ocr_with_accuracy('example_05.jpg', 'example_05.txt')
