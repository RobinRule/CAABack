
import boto3

import logging
logger = logging.getLogger(__name__)

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
import json

def getDynamoDBConnection(config=None, endpoint=None, port=None, local=False, use_instance_metadata=False):
    if local:
        db = boto3.resource(
            'dynamodb',
            endpoint_url=endpoint,
            port=port,
            aws_secret_access_key='caaSampleApp',
            aws_access_key_id='caaSampleApp')
    else:
        params = {}
        # Read from config file, if provided
        if config is not None:
            if config.has_option('dynamodb', 'region'):
                params['region_name'] = config.get('dynamodb', 'region')
            if config.has_option('dynamodb', 'endpoint'):
                params['endpoint_url'] = config.get('dynamodb', 'endpoint')

            if config.has_option('aws_credential', 'aws_access_key_id'):
                params['aws_access_key_id'] = config.get('aws_credential', 'aws_access_key_id')
                params['aws_secret_access_key'] = config.get('aws_credential', 'aws_secret_access_key')

        # Use the endpoint specified on the command-line to trump the config file
        if endpoint is not None:
            params['endpoint_url'] = endpoint
            if 'region_name' in params:
                del params['region_name']

        # Only auto-detect the DynamoDB endpoint if the endpoint was not specified through other config
        if 'host' not in params and use_instance_metadata:
            response = urlopen('http://169.254.169.254/latest/dynamic/instance-identity/document').read()
            doc = json.loads(response);
            params['endpoint_url'] = 'dynamodb.%s.amazonaws.com' % (doc['region'])
            if 'region' in params:
                del params['region_name']
        db = boto3.resource("dynamodb", **params)

    return db

def createCasesTable(db):
    try:
        casesTable = db.create_table(
            TableName = 'Cases',
            KeySchema=[
                {
                    'AttributeName' : 'caseId',
                    'KeyType' : 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName' : 'caseId',
                    'AttributeType' : 'N'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 20,
                'WriteCapacityUnits': 20
            }
        )
    except JSONResponseError as jre:
        try:
            casesTable = db.Table('Cases')
        except Exception as e:
            logger.exception("Cases Table doesn't exist.")
    finally:
        return casesTable

#parse command line args for credentials and such
#for now just assume local is when args are empty
