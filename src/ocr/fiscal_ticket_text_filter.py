# This script can filter the fiscal ticket text read from ocr
def filter_text(text):
    text = text.upper()
    text = text.replace('  ', ' ')
    text = text.replace('\'', '')
    text = text.replace(',,', ',')
    text = text.replace(',.', ',')
    text = text.replace('.,', ',')
    text = text.replace('..', '.')
    text = text.replace(' ,', ',')
    text = text.replace(' .', '')
    text = text.replace(' !', '')
    text = text.replace(' :', ':')
    text = text.replace('_', '')
    text = text.replace('-—', '—')
    text = text.replace('—-', '—')
    text = text.replace('"', '')

    for __ in range(50):
        text = text.replace('\n:', '\n')
        text = text.replace('\n-', '\n')
        text = text.replace('\n—', '\n')
        text = text.replace('\n ', '\n')

    text = text.replace('\n-', '\n')
    text = text.replace('VUL ITEM', 'VL ITEM')
    text = text.replace('ITEMM', 'ITEM')
    text = text.replace('ITENM', 'ITEM')
    text = text.replace('ACRESCIHO', 'ACRESCIMO')
    text = text.replace('HTTPS: ', 'HTTPS:')
    text = text.replace('HTTP: ', 'HTTP:')
    text = text.replace('HTTPS://UWW.', 'HTTPS://WWW.')
    text = text.replace('HTTPS://WUW.', 'HTTPS://WWW.')
    text = text.replace('HTTPS://WWU.', 'HTTPS://WWW.')
    text = text.replace('HTTPS://UUW.', 'HTTPS://WWW.')
    text = text.replace('HTTPS://WUU.', 'HTTPS://WWW.')
    text = text.replace('HTTPS://UUU.', 'HTTPS://WWW.')
    text = text.replace('HTTP://UWW.', 'HTTP://WWW.')
    text = text.replace('HTTP://WUW.', 'HTTP://WWW.')
    text = text.replace('HTTP://WWU.', 'HTTP://WWW.')
    text = text.replace('HTTP://UUW.', 'HTTP://WWW.')
    text = text.replace('HTTP://WUU.', 'HTTP://WWW.')
    text = text.replace('HTTP://UUU.', 'HTTP://WWW.')
    text = text.replace('CARTADON', 'CARTAOON')

    for __ in range(10):
        text = text.replace('0O0', '00')
        text = text.replace('0O1', '01')
        text = text.replace('0O2', '02')
        text = text.replace('0O3', '03')
        text = text.replace('0O4', '04')
        text = text.replace('0O5', '05')
        text = text.replace('0O6', '06')
        text = text.replace('0O7', '07')
        text = text.replace('0O8', '08')
        text = text.replace('0O9', '09')

        text = text.replace('OO0', '00')

        text = text.replace('O00', '00')
        text = text.replace('O01', '01')
        text = text.replace('O02', '02')
        text = text.replace('O03', '03')
        text = text.replace('O04', '04')
        text = text.replace('O05', '05')
        text = text.replace('O06', '06')
        text = text.replace('O07', '07')
        text = text.replace('O08', '08')
        text = text.replace('O09', '09')

        text = text.replace('0C0', '00')
        text = text.replace('0C1', '01')
        text = text.replace('0C2', '02')
        text = text.replace('0C3', '03')
        text = text.replace('0C4', '04')
        text = text.replace('0C5', '05')
        text = text.replace('0C6', '06')
        text = text.replace('0C7', '07')
        text = text.replace('0C8', '08')
        text = text.replace('0C9', '09')

        text = text.replace('CC0', '00')

        text = text.replace('C00', '00')
        text = text.replace('C01', '01')
        text = text.replace('C02', '02')
        text = text.replace('C03', '03')
        text = text.replace('C04', '04')
        text = text.replace('C05', '05')
        text = text.replace('C06', '06')
        text = text.replace('C07', '07')
        text = text.replace('C08', '08')
        text = text.replace('C09', '09')

    return text
