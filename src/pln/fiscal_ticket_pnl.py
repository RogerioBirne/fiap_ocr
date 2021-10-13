import re
from pycpfcnpj import cpfcnpj

__ARRAY_REGEX_CPF__ = ['[0-9]{3}\.?[0-9]{3}\.?[0-9]{3}\-?[0-9]{2}']
__ARRAY_REGEX_CNPJ__ = ['[0-9]{2}\.?[0-9]{3}\.?[0-9]{3}\/?[0-9]{4}\-?[0-9]{2}']
__ARRAY_REGEX_TOTAL__ = ['([Tt][Oo][Tt][Aa][Ll]).*([R$]).*([-+]?\d*\.?\d+|[-+]?\d+)',
                         '([Vv][Aa][Ll][Oo][Rr]).*([R$]).*([-+]?\d*\.?\d+|[-+]?\d+)',
                         '([Pp][Aa][Gg][Aa][Rr]).*([R$]).*([-+]?\d*\.?\d+|[-+]?\d+)']
__ARRAY_REGEX_ITEMS__ = ['([-+]?\d*\.?\d+|[-+]?\d+).*([Uu][Nn]).*([-+]?\d*\.?\d+|[-+]?\d+)']
__NUMBERS_POINTS__ = '0123456789.,'
__NEW_LINE__ = '\n'
__UNIT__ = 'UN'
__CPF_SIZE__ = 11
__CNPJ_MIN_SIZE__ = 14
__CNPJ_MAX_SIZE__ = 18


def extract_data(text):
    structured_text = structure_text(text)
    return apply_extraction(structured_text)


def structure_text(text):
    new_text = ''
    for line in text.split(__NEW_LINE__):
        if len(line) > 5:
            if __UNIT__ in line[:5]:
                new_text = new_text[:len(new_text) - 2] + line + __NEW_LINE__
            else:
                new_text = new_text + line + __NEW_LINE__
    return new_text


def apply_extraction(text):
    result = {}
    array_text = text.split(__NEW_LINE__)
    result['customer'] = extract_cpf(array_text)
    result['company'] = extract_cnpj(array_text)
    result['items'] = extract_items(array_text)
    result['total'] = extract_total(array_text)
    return result


def extract_cpf(array_text):
    for line in array_text:
        for regex in __ARRAY_REGEX_CPF__:
            matches = re.search(regex, line)
            if matches:
                value = matches.group(0)
                if cpfcnpj.validate(value):
                    if __CPF_SIZE__ <= len(value) <= __CNPJ_MIN_SIZE__:
                        if len(value) == __CPF_SIZE__:
                            return format_cpf(value)
                        return value
    return ''


def extract_cnpj(array_text):
    for line in array_text:
        for regex in __ARRAY_REGEX_CNPJ__:
            matches = re.search(regex, line)
            if matches:
                value = matches.group(0)
                if cpfcnpj.validate(value):
                    if __CNPJ_MIN_SIZE__ <= len(value) <= __CNPJ_MAX_SIZE__:
                        if len(value) == __CNPJ_MIN_SIZE__:
                            return format_cnpj(value)
                        return value
    return ''


def extract_items(array_text):
    items = []
    for line in array_text:
        for regex in __ARRAY_REGEX_ITEMS__:
            matches = re.search(regex, line)
            if matches:
                value = matches.group(0)
                if value != '':
                    items.append(value)
    return items


def extract_total(array_text):
    for line in array_text:
        for index, regex in enumerate(__ARRAY_REGEX_TOTAL__):
            matches = re.search(regex, line)
            if matches:
                value = matches.group(0)
                if value != '':
                    return only_numbers_and_points(value)
    return ''


def only_numbers_and_points(text):
    value = ''
    for character in text:
        if character in __NUMBERS_POINTS__:
            value += character
    return value


def format_cnpj(cnpj):
    return '{}.{}.{}/{}-{}'.format(cnpj[:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:])


def format_cpf(cpf):
    return '{}.{}.{}-{}'.format(cpf[:3], cpf[3:6], cpf[6:9], cpf[9:])