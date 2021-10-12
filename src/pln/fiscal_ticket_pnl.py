import re
from pycpfcnpj import cpfcnpj

array_regex_cpf = ["[0-9]{3}\.?[0-9]{3}\.?[0-9]{3}\-?[0-9]{2}"]
array_regex_cnpj = ["[0-9]{2}\.?[0-9]{3}\.?[0-9]{3}\/?[0-9]{4}\-?[0-9]{2}"]
array_regex_total = ["([Tt][Oo][Tt][Aa][Ll]).*([R$]).*([-+]?\d*\.?\d+|[-+]?\d+)",
                     "([Vv][Aa][Ll][Oo][Rr]).*([R$]).*([-+]?\d*\.?\d+|[-+]?\d+)",
                     "([Pp][Aa][Gg][Aa][Rr]).*([R$]).*([-+]?\d*\.?\d+|[-+]?\d+)"]
array_regex_itens = ["([-+]?\d*\.?\d+|[-+]?\d+).*([Uu][Nn]).*([-+]?\d*\.?\d+|[-+]?\d+)"]
numbers_points = "0123456789.,"


def extract_data(text):
    structured_text = structure_text(text)
    return apply_extraction(structured_text)


def structure_text(text):
    new_text = ""
    for l in text.split("\n"):
        if len(l) > 5:
            if "UN" in l[:5]:
                new_text = new_text[:len(new_text) - 2] + l + "\n"
            else:
                new_text = new_text + l + "\n"
    return new_text


def apply_extraction(text):
    result = {}
    array_text = text.split("\n")
    result["customer"] = extract_cpf(array_text)
    result["company"] = extract_cnpj(array_text)
    result["itens"] = extract_itens(array_text)
    result["total"] = extract_total(array_text)
    return result


def extract_cpf(array_text):
    for line in array_text:
        for r in array_regex_cpf:
            m = re.search(r, line)
            if m:
                value = m.group(0)
                if cpfcnpj.validate(value):
                    if len(value) >= 11 and len(value) <= 14:
                        if len(value) == 11:
                            return format_cpf(value)
                        return value
    return ""


def extract_cnpj(array_text):
    for line in array_text:
        for r in array_regex_cnpj:
            m = re.search(r, line)
            if m:
                value = m.group(0)
                if cpfcnpj.validate(value):
                    if len(value) >= 14 and len(value) <= 18:
                        if len(value) == 14:
                            return format_cnpj(value)
                        else:
                            return value
    return ""


def extract_itens(array_text):
    itens = []
    for line in array_text:
        for r in array_regex_itens:
            m = re.search(r, line)
            if m:
                value = m.group(0)
                if value != "":
                    itens.append(value)
    return itens


def extract_total(array_text):
    for line in array_text:
        if "TOTAL" in line:
            print(line)
        for index, r in enumerate(array_regex_total):
            m = re.search(r, line)
            if m:
                value = m.group(0)
                if value != "":
                    return only_numbers_and_points(value)
    return ""


def only_numbers_and_points(text):
    value = ""
    for c in text:
        if c in numbers_points:
            value += c
    return value


def format_cnpj(cnpj):
    return '{}.{}.{}/{}-{}'.format(cnpj[:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:])


def format_cpf(cpf):
    return '{}.{}.{}-{}'.format(cpf[:3], cpf[3:6], cpf[6:9], cpf[9:])
