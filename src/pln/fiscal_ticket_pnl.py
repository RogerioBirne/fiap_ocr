import re
from pycpfcnpj import cpfcnpj

exampleText = """MONTEIRO BRAGA CONSULTORIA EBMPRESARIAL LTDA
DEALERNET

R. ANDRÉ L. R. DAFONTE, 25/20 - SALA 601

42.700-000 L. DEFREITAS - DA

CNPJ 88.876.957/0001-47

TE :166994360-NO UFIDA

IM:3SENTO

25/06/2012 14:36:29 — CCF:000002 C00:000005

CNPJ/CPF consumidor:393.285.650-30

NOME:URSO DA GATUCADA

ENO:RUA ALMIRANTE SARROSO, Nº40, VITORIA, CEP:S4

0275240, SALVADOR-BA

ITEM CÓDIGO DESCRIÇÃO QTO.UN-.VL UNIT( R$) ST VL-

I1TEMÍ RS)

001 13435708 ABRACADEIRA 90.5
1UN X 9,28 F1 9,289

TOTAL R$ 9,28

DINHEIRO 9.28

MD-S:cbf73ccOSfffc7aaSfabacbadofI9O0O2d

PY10000005390 N$:0093976-1

MINAS LEGAL 14552558000194 25062012 928

BEMATECH MP-2100 TW FI ECF-I1F

VERSÃO:01.00.01 ECF:001 LJ:0001

QQGQARARAGRAQQNOY U 28/06/2012 14:37:05

FAS : ENULADOR sº"""

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
