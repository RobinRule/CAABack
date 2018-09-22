import os
import sys
from flask import Flask
import json
from enum import Enum

# Create Flask application
APP = Flask(__name__)
APP_NAME = "CAA Management Service"

APP_VERSION = 1.0
URL_VERSION = "/api/v{}".format(APP_VERSION)

APP.debug=True

SRC_PATH = os.path.dirname(os.path.abspath(__file__))

class Errors(Enum):
	ErrorNoSuchId = "ErrorNoSuchId"
	ErrorRequestIllFormated = "ErrorRequestIllFormated"
	ErrorNotAuthoriedOperation = "ErrorNotAuthoriedOperation"

#declare in here, initialized in server.py
CFG = {}
ARGS = {}