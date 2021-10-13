from flask import Flask, flash, request, redirect, url_for, send_from_directory, jsonify
from datetime import datetime
from src.ocr import fiscal_ticket_ocr
from src.pln import fiscal_ticket_pnl
from src import RESOURCES_PATH
import os

__IMAGES_RECEIVED_PATH__ = '{}/images_received'.format(RESOURCES_PATH)

app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def upload_file():
    if validate_request(request):
        path = receive_file(request)
        text = fiscal_ticket_ocr.convert_file_image_to_string(path)
        return fiscal_ticket_pnl.extract_data(text)


def validate_request(req):
    return len(req.files) == 1 and req.files['file'] is not None


def receive_file(req):
    file = req.files['file']
    if not os.path.exists(__IMAGES_RECEIVED_PATH__):
        os.makedirs(__IMAGES_RECEIVED_PATH__)

    now = datetime.now()
    path = '{}/{}_{}'.format(__IMAGES_RECEIVED_PATH__, now.strftime('%d-%m-%y-%H-%M-%S'), file.filename)

    file.save(path)
    file.close()
    return path


if __name__ == '__main__':
    app.run()
