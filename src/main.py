from flask import Flask, flash, request, redirect, url_for, send_from_directory, jsonify
from datetime import datetime

from src import RESOURCES_PATH
from src.ocr.fiscal_ticket_ocr import FiscalTicketOcr
from src.ocr.fiscal_ticket_pnl import FiscalTicketPnl

app = Flask(__name__)

ALLOWED_EXTENTIONS = {'.pdf', '.png', '.jpg', '.jpeg', '.txt'}


def allowed_file(filename):
    index = filename.find('.')
    ext = filename[index:]
    if ext in ALLOWED_EXTENTIONS:
        return True
    return False


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files["file"]
    if file and allowed_file(file.filename):
        path = RESOURCES_PATH + datetime.now().strftime("%d-%m-%y-%H-%M-%S") + "_" + file.filename
        file.save(path)
        file.close()
        fiscal_ticket_ocr = FiscalTicketOcr(debug_model=True)
        fiscal_ticket_pnl = FiscalTicketPnl()
        fiscal_ticket = fiscal_ticket_ocr.convert_file_image_to_string(path)
        return fiscal_ticket_pnl.extract_data(fiscal_ticket)


app.run()
