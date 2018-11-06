# -*- coding: utf-8 -*-

"""
    server.py
    Center point of CAA Management System.
    Example usage: python server.py
    Authur:
        !!!! Add your name here in alphabeta order!!!!!
        Zhiyu Feng{@zf499@nyu.edu}
"""

import os, argparse
import global_var
import json
from configparser                   import ConfigParser

import logging
logger = logging.getLogger(__name__)

# Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_409_CONFLICT = 409


"""
   Configure the application according to the command line args and config files
"""


parser = argparse.ArgumentParser(description='Run the CAA Management app', prog='server.py')
parser.add_argument('--config', help='Path to the config file containing application settings. Cannot be used if the CONFIG_FILE environment variable is set instead')
parser.add_argument('--mode', help='Whether to connect to a DynamoDB service endpoint, or to connect to DynamoDB Local. In local mode, no other configuration ' \
                    'is required. In service mode, AWS credentials and endpoint information must be provided either on the command-line or through the config file.',
                    choices=['local', 'service'], default='service')
parser.add_argument('--endpoint', help='An endpoint to connect to (the host name - without the http/https and without the port). ' \
                    'When using DynamoDB Local, defaults to localhost. If the USE_EC2_INSTANCE_METADATA environment variable is set, reads the instance ' \
                    'region using the EC2 instance metadata service, and contacts DynamoDB in that region.')
parser.add_argument('--port', help='The port of DynamoDB Local endpoint to connect to.  Defaults to 8000', type=int)
parser.add_argument('--serverPort', help='The port for this Flask web server to listen on.  Defaults to 5000 or whatever is in the config file. If the SERVER_PORT ' \
                    'environment variable is set, uses that instead.', type=int)
parser.add_argument('--log', help='path to log file. ./{} by default'.format(global_var.APP_NAME), default='./{}.log'.format(global_var.APP_NAME), type=str)
parser.add_argument('--loglevel', help='logging level, ERROR by default', default='ERROR', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])

global_var.ARGS = parser.parse_args()

# read in config file
configFile = global_var.ARGS.config
global_var.CFG = None
if 'CONFIG_FILE' in os.environ:
    if configFile is not None:
        raise Exception('Cannot specify --config when setting the CONFIG_FILE environment variable')
    configFile = os.environ['CONFIG_FILE']
if configFile is not None:
    global_var.CFG = ConfigParser()
    global_var.CFG.read(configFile)

SVR_PORT = global_var.ARGS.serverPort
if global_var.CFG is not None:
    if global_var.CFG.has_option('flask', 'secret_key'):
        global_var.APP.secret_key = global_var.CFG.get('flask', 'secret_key')
    if SVR_PORT is None:
        if global_var.CFG.has_option('flask', 'serverPort'):
            SVR_PORT = global_var.CFG.get('flask', 'serverPort')

# Default to environment variables for server port - easier for elastic beanstalk configuration
if 'SERVER_PORT' in os.environ:
    SVR_PORT = int(os.environ['SERVER_PORT'])

if SVR_PORT is None:
    SVR_PORT = 5000


from flask import Flask, jsonify, request, json, flash
import fileinput
from business.CaseBusiness import CaseBusiness
from business.UserBusiness import UserBusiness
######################################################################
# GET INDEX
######################################################################
@global_var.APP.route('/')
def index():
    logger.info("Sending root static file...")
    return global_var.APP.send_static_file('swagger/index.html')

@global_var.APP.route('/lib/<path:path>')
def send_lib(path):
    return global_var.APP.send_static_file('swagger/lib/' + path)

@global_var.APP.route('/specification/<path:path>') #this is for the PortfolioMgmt Swagger api
def send_specification(path):
    return global_var.APP.send_static_file('swagger/specification/' + path)

@global_var.APP.route('/images/<path:path>')
def send_images(path):
    return global_var.APP.send_static_file('swagger/images/' + path)

@global_var.APP.route('/css/<path:path>')
def send_css(path):
    return global_var.APP.send_static_file('swagger/css/' + path)

@global_var.APP.route('/fonts/<path:path>')
def send_fonts(path):
    return global_var.APP.send_static_file('swagger/fonts/' + path)

@global_var.APP.route(global_var.URL_VERSION)
def index_api():
    return jsonify(name=global_var.APP_NAME, version=global_var.APP_VERSION, url='/cases'), HTTP_200_OK

# authorize request's access token
def authorize(func):
    def func_wrapper(*args, **kwargs):
        headers = request.headers
        try:
            auth = headers['cognito-auth']
        except Exception as e:
            return reply( { "error" : "Missing cognito-auth header"}, HTTP_400_BAD_REQUEST)

        try:
            auth = headers['cognito-auth']
            requesterId = UserBusiness.checkToken(auth)
        except Exception as e:
            return reply( { "error" : "InvalidToken" }, HTTP_400_BAD_REQUEST)

        kwargs['requesterId'] = requesterId
        return func(*args, **kwargs)

    func_wrapper.__name__ = func.__name__
    return func_wrapper

######################################################################
# Upload a resource
######################################################################
@global_var.APP.route(global_var.URL_VERSION+"/resources/<resource_id>", methods=['POST'])
@authorize
def upload_resource(resource_id, requesterId):
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    filename = secure_filename(file.filename)
    file_path = os.path.join(global_var.CFG['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    return reply( ResourceBusiness.uploadResource(requesterId, resource_id, file_path), HTTP_200_OK)


######################################################################
# Get User
######################################################################
@global_var.APP.route(global_var.URL_VERSION+"/users/<user_id>/", methods=['GET'])
@authorize
def get_user(user_id, requesterId):
    return reply( UserBusiness.getUser(requesterId, user_id), HTTP_200_OK)


######################################################################
# ADD User
######################################################################
@global_var.APP.route(global_var.URL_VERSION+"/users/", methods=['POST'])
@authorize
def add_user(requesterId):
    try:
        payload = json.loads(request.data)
    except Exception as e:
        logger.exception("Failed to load data")
        return reply( {}, HTTP_400_BAD_REQUEST)

    return reply( UserBusiness.addUser(requesterId, payload), HTTP_200_OK)


######################################################################
# UPDATE a User
######################################################################
@global_var.APP.route(global_var.URL_VERSION+"/users/", methods=['PUT'])
@authorize
def update_user(requesterId):
    try:
        payload = json.loads(request.data)
    except Exception as e:
        logger.exception("Failed to load data")
        return reply( {}, HTTP_400_BAD_REQUEST)
    raise NotImplementedError()
    return reply( UserBusiness.updateUser(payload), HTTP_200_OK)



######################################################################
# CREATE a users transaction
######################################################################
@global_var.APP.route(global_var.URL_VERSION+"/users/<user_id>/", methods=['POST'])
@authorize
def create_user_transaction(user_id, requesterId):
    try:
        payload = json.loads(request.data)
    except Exception as e:
        logger.exception("Failed to load data")
        return reply( {}, HTTP_400_BAD_REQUEST)

    return reply(
        UserBusiness.createTransaction(
            requesterId=requesterId,
            targetUserId=user_id,
            winSize=payload["window_size"]#,
            # specs=payload["search_specs"]
        ),
        HTTP_200_OK)            


######################################################################
# GET users by transaction_id
######################################################################
@global_var.APP.route(global_var.URL_VERSION+"/users/transaction/<transaction_id>/", methods=['GET'])
@authorize
def get_users_by_transaction(transaction_id, requesterId):
    return reply( UserBusiness.getUsersByTransacId(requesterId, transaction_id), HTTP_200_OK)




######################################################################
# ADD a case
######################################################################
@global_var.APP.route(global_var.URL_VERSION+"/cases/", methods=['POST'])
@authorize
def add_case():
    try:
        payload = json.loads(request.data)
    except Exception as e:
        logger.exception("Failed to load data")
        return reply( {}, HTTP_400_BAD_REQUEST)
    return reply( CaseBusiness.addCase(payload), HTTP_200_OK)

######################################################################
# DELETE a case
######################################################################
@global_var.APP.route(global_var.URL_VERSION+"/cases/<user_id>/<case_id>", methods=['DELETE'])
@authorize
def delete_case(user_id, case_id, token):
    return reply( {"status": CaseBusiness.delCase(user_id, case_id)}, HTTP_200_OK)

######################################################################
# UPDATE a case
######################################################################
@global_var.APP.route(global_var.URL_VERSION+"/cases/", methods=['PUT'])
@authorize
def update_case(token):
    try:
        payload = json.loads(request.data)
    except Exception as e:
        logger.exception("Failed to load data")
        return reply( {}, HTTP_400_BAD_REQUEST)
    return reply( CaseBusiness.updateCase(payload), HTTP_200_OK)

######################################################################
# GET a case by id
######################################################################
@global_var.APP.route(global_var.URL_VERSION+"/cases/<user_id>/<case_id>/", methods=['GET'])
@authorize
def get_case(user_id, case_id, token):
    return reply( CaseBusiness.getCase(user_id, case_id), HTTP_200_OK)

######################################################################
# CREATE a transaction
######################################################################
@global_var.APP.route(global_var.URL_VERSION+"/cases/<user_id>/", methods=['POST'])
@authorize
def create_case_transaction(user_id, token):
    try:
        payload = json.loads(request.data)
    except Exception as e:
        logger.exception("Failed to load data")
        return reply( {}, HTTP_400_BAD_REQUEST)
    
    return reply(
        CaseBusiness.createTransaction(
            callerToken="1",
            userId=user_id,
            winSize=payload["window_size"],
            specs=payload["search_specs"]
        ),
        HTTP_200_OK)

######################################################################
# GET cases by transaction_id
######################################################################
@global_var.APP.route(global_var.URL_VERSION+"/cases/transaction_id/<transaction_id>/", methods=['GET'])
@authorize
def get_cases_by_transaction(transaction_id, token):
    return reply( CaseBusiness.getCasesByTransacId("1", transaction_id), HTTP_200_OK)




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
            global_var.APP.logger.error('Missing key in data: {0}'.format(k))
            return False
    return True

if __name__ == '__main__':
    logLevel = global_var.ARGS.loglevel
    logLevelMap = {
        'DEBUG'    : logging.DEBUG,
        'INFO'     : logging.INFO,
        'WARNING'  : logging.WARNING,
        'ERROR'    : logging.ERROR,
        'CRITICAL' : logging.CRITICAL
    }
    logging.basicConfig(filename=global_var.ARGS.log, level=logLevelMap[logLevel],
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        datefmt='%m-%d %H:%M')
    global_var.APP.run(host="0.0.0.0", port=SVR_PORT)
