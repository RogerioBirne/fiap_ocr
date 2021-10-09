from src import RESOURCES_PATH
from ocr.fiscal_ticket_ocr import FiscalTicketOcr
from ocr.fiscal_ticket_pnl import FiscalTicketPnl
import textdistance


if __name__ == '__main__':
    fiscal_ticket_ocr = FiscalTicketOcr(debug_model=True)
    fiscal_ticket_pnl = FiscalTicketPnl()
    fiscal_ticket = fiscal_ticket_ocr.convert_file_image_to_string('{}/images/example_10.jpg'.format(RESOURCES_PATH))

    digit_text = 'CIA BRASILEIRA DE DISTRIBUICAO\nEX - RICARDO JAFFET\nAVENIDA DOUTOR RICARDO JAFFET, 1501\nVILA SANTA EULA, SAO PAULO - SP\nDUCUMENTO AUXILIAR DA NOTA FISCAL DE CONSUMIDER ELETRôNICA\n# | COD | DESC | QTD | UN | VL UN R$ | (VLTR R$)* | VL ITEM R$\n----------------------------------------------------------------\n001 00000000120289 DET YPE 500ML 6 UN X 2,19 (4,23)  13,14\ndesconto sobre item  -0,60\n002 00000000105316 GUARD PAP KIT 23X22 4 UN X 2,09 (2,74)  8,36\ndesconto sobre item  -0,80\n003 00000001239774 TORCI PIME MEXI 100G 2 UN X 3,39 (1,81) 6,78\n004 00000001819038 PAO SIRIO INTEG 320G\n1 UN 11,79 (3,16)  11,79\n005 00000007094651 AMEND JAP YOKI 500G 1 UN X 10,29 (3,23) 10,29\n006 00000004346968 COCA ZERO 2L 1 UN X 8,59 (2.82)  8,59\n007 00000001469349 SACOLA VERDE SP 48X5 2 UN 0,11 (0,08)  0,22\n008 00000001469332 SACOLA CINZ 48X55 2 UN 0,11 (0,08)  0,22\nQTD. TOTAL DE ITEMS  8\nVALOR TOTAL R$  59,39\nDESCONTO R$  1,40\nACRESCIMO R$  0,00\nVALOR A PAGAR R$  57,99\nCARTAOON  57,99\nConsulte pela Chave de Acesso em\nhttps://www.nfce.fazenda.sp.gov/consulta\n3521 0947 5084 1105 8154 6516 4000 0127 8218 5803 8551\nCONSUMIDOR - CPF 228.082.988-62 FERNA\nNDA CARLI\n\nNFC-e 000012782 Seria 164 14/09/2021 18:38\n:30\nProtocolo de autorizacao: 135210501050365\nData de autorizacao 14/09/2021 18:38:30\n\n20210914135916400044182\nPDV:164 LJ:1359 Ve:122 COO:44182\nSIACFISC.EXE V:13 Op:013591359 SELF CHECKOUT\nINF01: FERNANDA CARLI\nINF02: Clube Extra\nVoce economuzou em descontos 1,40\nMASTERCARD ************4622\nAUT:274115 NSU:164982 DOC:003456328\nVENDA CREDITO A VISTA\nVALOR:  57,99 CTR:09469084119\nTrib aprox R$ Fed 8,58 Est 9,57 IBPT'
    normalized_similarity = textdistance.hamming.normalized_similarity(digit_text, fiscal_ticket)
    print('normalized_similarity', normalized_similarity)
