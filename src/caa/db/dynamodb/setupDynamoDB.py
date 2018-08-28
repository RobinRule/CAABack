# Copyright 2014. Amazon Web Services, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# from boto3.exception         import JSONResponseError
# from boto3.dynamodb2.fields  import KeysOnlyIndex
# from boto3.dynamodb2.fields  import GlobalAllIndex
# from boto3.dynamodb2.fields  import HashKey
# from boto3.dynamodb2.fields  import RangeKey
# from boto3.dynamodb2.layer1  import DynamoDBConnection
# from boto3.dynamodb2.table   import Table

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
            aws_secret_access_key='ticTacToeSampleApp',
            aws_access_key_id='ticTacToeSampleApp')
    else:
        params = {}
        # Read from config file, if provided
        if config is not None:
            if config.has_option('dynamodb', 'region'):
                params['region_name'] = config.get('dynamodb', 'region')
            if config.has_option('dynamodb', 'endpoint'):
                params['endpoint_url'] = config.get('dynamodb', 'endpoint')

            if config.has_option('dynamodb', 'aws_access_key_id'):
                params['aws_access_key_id'] = config.get('dynamodb', 'aws_access_key_id')
                params['aws_secret_access_key'] = config.get('dynamodb', 'aws_secret_access_key')

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
    print("Getting table 5")
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
