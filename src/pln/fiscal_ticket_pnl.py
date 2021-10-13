import re
from pycpfcnpj import cpfcnpj

__ARRAY_REGEX_CPF__ = ['[0-9]{3}\.?[0-9]{3}\.?[0-9]{3}\-?[0-9]{2}']
__ARRAY_REGEX_CNPJ__ = ['[0-9]{2}\.?[0-9]{3}\.?[0-9]{3}\/?[0-9]{4}\-?[0-9]{2}']
__ARRAY_REGEX_TOTAL__ = ['([Tt][Oo][Tt][Aa][Ll]).*([R$]).*([-+]?\d*\.?\d+|[-+]?\d+)',
                         '([Vv][Aa][Ll][Oo][Rr]).*([R$]).*([-+]?\d*\.?\d+|[-+]?\d+)',
                         '([Pp][Aa][Gg][Aa][Rr]).*([R$]).*([-+]?\d*\.?\d+|[-+]?\d+)']
__ARRAY_REGEX_ITEMS__ = ['([-+]?\d*\.?\d+|[-+]?\d+).*(( )|(\.))([Uu][Nn]).*([-+]?\d*\.?\d+|[-+]?\d+)',
                         '([-+]?\d*\.?\d+|[-+]?\d+).*(( )|(\.))([Uu][Nn])',
                         '([-+]?\d*\.?\d+|[-+]?\d+).*([Kk][Gg]).*([-+]?\d*\.?\d+|[-+]?\d+)',
                         '([-+]?\d*\.?\d+|[-+]?\d+).*([Kk][Gg])']
__NUMBERS_POINTS__ = '0123456789.,'
__NEW_LINE__ = '\n'
__UNIT__ = 'UN'
__KILOGRAM__ = 'KG'
__CPF_SIZE__ = 11
__CNPJ_MIN_SIZE__ = 14
__CNPJ_MAX_SIZE__ = 18


def extract_data(text):
    structured_text = __structure_text(text)
    return __apply_extraction(structured_text)


def __structure_text(text):
    new_text = ''
    for line in text.split(__NEW_LINE__):
        if len(line) > 5:
            if __UNIT__ in line[:5] or __KILOGRAM__ in line[:5]:
                new_text = new_text[:len(new_text) - 2] + line + __NEW_LINE__
            else:
                new_text = new_text + line + __NEW_LINE__
    return new_text


def __apply_extraction(text):
    result = {}
    array_text = text.split(__NEW_LINE__)
    result['customer'] = __extract_cpf(array_text)
    result['company'] = __extract_cnpj(array_text)
    result['items'] = __extract_items(array_text)
    result['total'] = __extract_total(array_text)
    return result


def __extract_cpf(array_text):
    for line in array_text:
        line = line.replace(' ', '')
        line = line.replace('.', '')
        line = line.replace(',', '')
        line = line.replace('-', '')
        line = line.replace('—', '')
        for regex in __ARRAY_REGEX_CPF__:
            matches = re.search(regex, line)
            if matches:
                value = matches.group(0)
                if cpfcnpj.validate(value):
                    if __CPF_SIZE__ <= len(value) <= __CNPJ_MIN_SIZE__:
                        if len(value) == __CPF_SIZE__:
                            return __format_cpf(value)
                        return value
    return ''


def __extract_cnpj(array_text):
    for line in array_text:
        line = line.replace(' ', '')
        line = line.replace('.', '')
        line = line.replace(',', '')
        line = line.replace('-', '')
        line = line.replace('—', '')
        line = line.replace('/', '')
        for regex in __ARRAY_REGEX_CNPJ__:
            matches = re.search(regex, line)
            if matches:
                value = matches.group(0)
                if cpfcnpj.validate(value):
                    if __CNPJ_MIN_SIZE__ <= len(value) <= __CNPJ_MAX_SIZE__:
                        if len(value) == __CNPJ_MIN_SIZE__:
                            return __format_cnpj(value)
                        return value
    return ''


def __extract_items(array_text):
    items = []
    for line in array_text:
        item = __extract_item(line)
        if item is not None:
            items.append(item)
    return items


def __extract_item(line):
    for regex in __ARRAY_REGEX_ITEMS__:
        matches = re.search(regex, line)
        if matches:
            value = matches.group(0)
            if value != '':
                return value
    return None


def __extract_total(array_text):
    for line in array_text:
        for index, regex in enumerate(__ARRAY_REGEX_TOTAL__):
            matches = re.search(regex, line)
            if matches:
                value = matches.group(0)
                if value != '':
                    return __only_numbers_and_points(value)
    return ''


def __only_numbers_and_points(text):
    value = ''
    for character in text:
        if character in __NUMBERS_POINTS__:
            value += character
    return value


def __format_cnpj(cnpj):
    return '{}.{}.{}/{}-{}'.format(cnpj[:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:])


def __format_cpf(cpf):
    return '{}.{}.{}-{}'.format(cpf[:3], cpf[3:6], cpf[6:9], cpf[9:])
