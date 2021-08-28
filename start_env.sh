#!/bin/bash

## This script start virtual environment and install all required python modules

virtualenv venv

source venv/bin/activate

pip install -r path/to/requirements.txt
