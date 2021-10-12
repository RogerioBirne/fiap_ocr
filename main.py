from flask import Flask, flash, request, redirect, url_for, send_from_directory, jsonify
from datetime import datetime
from src.ocr import fiscal_ticket_ocr
from src.pln import fiscal_ticket_pnl

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if validate_request(request):
        path = receive_file(request)
        text = fiscal_ticket_ocr.convert_file_image_to_string(path)
        return fiscal_ticket_pnl.extract_data(text)


def validate_request(req):
    return len(req.files) == 1 and req.files["file"] is not None


def receive_file(req):
    file = req.files["file"]
    path = "resources/imagestest/" + datetime.now().strftime("%d-%m-%y-%H-%M-%S") + "_" + file.filename
    file.save(path)
    file.close()
    return path


app.run()
