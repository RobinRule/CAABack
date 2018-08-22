import os
import sys
from flask import Flask
import json

# Create Flask application
APP = Flask(__name__)
APP_NAME = "CAA Management Service"

APP_VERSION = 1.0
URL_VERSION = "/api/v{}".format(APP_VERSION)

APP.debug=True

SRC_PATH = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(SRC_PATH, "config.json")) as f:
    CFG = json.load(f)