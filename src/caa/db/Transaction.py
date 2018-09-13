
from .DBManager import DBManager
from datetime import datetime
from dateutil.parser import parse as timeParse
from boto3.dynamodb.conditions import Key, Attr
import logging


logger = logging.getLogger(__name__)

class Transaction(object):
    """docstring for Transaction"""
    FIELD_LIST = [
        'transactionId',
        'caseIds'
    ]
    
    def __getattr__(self, key):
        return self.attrMap[key]

    def __setattr__(self, key, val):
        self.attrMap[key] = val

    def __init__(self, jsonObj=None):
        self.attrMap = {}
        if jsonObj is not None:
            for key, val in jsonObj.iteritems():
                if key in Transaction.FIELD_LIST:
                    self.attrMap[key] = jsonObj[key]
        
