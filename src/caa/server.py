# -*- coding: utf-8 -*-

"""
    server.py
    Center point of CAA Management System.
    Example usage: python server.py
    Authur:
        !!!! Add your name here in alphabeta order!!!!!
        Zhiyu Feng{@zf499@nyu.edu}
"""

import os
from flask import Flask, jsonify, request, json
import fileinput
from business.CaseBusiness import CaseBusiness
from global_var import APP, APP_NAME, APP_VERSION, URL_VERSION
import json


# Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_409_CONFLICT = 409


######################################################################
# GET INDEX
######################################################################
@APP.route('/')
def index():
    print "Sending root static file..."
    return APP.send_static_file('swagger/index.html')

@APP.route('/lib/<path:path>')
def send_lib(path):
    return APP.send_static_file('swagger/lib/' + path)

@APP.route('/specification/<path:path>') #this is for the PortfolioMgmt Swagger api
def send_specification(path):
    return APP.send_static_file('swagger/specification/' + path)

@APP.route('/images/<path:path>')
def send_images(path):
    return APP.send_static_file('swagger/images/' + path)

@APP.route('/css/<path:path>')
def send_css(path):
    return APP.send_static_file('swagger/css/' + path)

@APP.route('/fonts/<path:path>')
def send_fonts(path):
    return APP.send_static_file('swagger/fonts/' + path)

@APP.route(URL_VERSION)
def index_api():
    return jsonify(name=APP_NAME, version=APP_VERSION, url='/cases'), HTTP_200_OK


######################################################################
# RETRIEVE the a case by id
######################################################################
@APP.route(URL_VERSION+"/cases/<case_id>", methods=['GET'])
def get_case(case_id):
    """
    GET request at localhost:5000/api/v1/cases/<asset_id>
    """
    return reply( CaseBusiness.getCase(case_id), HTTP_200_OK)

@APP.route(URL_VERSION+"/cases", methods=['PUT'])
def add_case():
    """
    GET request at localhost:5000/api/v1/cases/<asset_id>
    """
    try:
        payload = json.loads(request.data)
    except:
        return reply( {}, HTTP_400_BAD_REQUEST)
    
    return reply( {"caseId": CaseBusiness.addCase(payload)}, HTTP_200_OK)

######################################################################
# UTILITY FUNCTIONS
######################################################################
def reply(message, rc):
    response = jsonify(message)
    response.headers['Content-Type'] = 'application/json'
    response.status_code = rc
    return response

def is_valid(data, keys=[]):
    for k in keys:
        if k not in data:
            #app.logger.error('Missing key in data: {0}'.format(k))
            return False
    return True

if __name__ == '__main__':
    APP.run()