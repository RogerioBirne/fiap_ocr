import json
import re

exampleText = """MONTEIRO BRAGA CONSULTORIA EBMPRESARIAL LTDA
DEALERNET

R. ANDRÉ L. R. DAFONTE, 25/20 - SALA 601

42.700-000 L. DEFREITAS - DA

CNPI163.356.000/0001 -49

TE :166994360-NO UFIDA

IM:3SENTO

25/06/2012 14:36:29 — CCF:000002 C00:000005

CNPJ/CPF consumiídor:111.111.111-11

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
array_regex_total = ["([Tt][Oo][Tt][Aa][Ll]).*([-+]?\d*\.?\d+|[-+]?\d+)"]
array_regex_itens = [""]


class FiscalTicketPnl:
    def extract_data(self, text):
        text = exampleText
        clean_text = self.clean_text(text)
        result = self.apply_extraction(clean_text)
        return result

    @staticmethod
    def clean_text(text):
        new = "".join([s for s in text.splitlines(True) if s.strip("\r\n")])
        return new

    def apply_extraction(self, text):
        result = {}
        array_text = text.split("\n")
        result["cpf"] = self.extract_cpf(array_text)
        result["cnpj"] = self.extract_cnpj(array_text)
        result["total"] = self.extract_total(array_text)
        return result

    def extract_cpf(self, array_text):
        for line in array_text:
            for r in array_regex_cpf:
                m = re.search(r, line)
                if m:
                    value = m.group(0)
                    return value
        return ""

    def extract_cnpj(self, array_text):
        for line in array_text:
            for r in array_regex_cnpj:
                m = re.search(r, line)
                if m:
                    value = m.group(0)
                    return value
        return ""

    def extract_total(self, array_text):
        for line in array_text:
            for index, r in enumerate(array_regex_total):
                m = re.search(r, line)
                if m:
                    value = m.group(0)
                    if index + 1 >= len(array_regex_total):
                        return value
        return ""
