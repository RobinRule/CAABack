
from .DBManager import DBManager
from .Case import Case
from datetime import datetime
from dateutil.parser import parse as timeParse
from boto3.dynamodb.conditions import Key, Attr
import logging
import uuid

logger = logging.getLogger(__name__)

class Transaction(object):
    """docstring for Transaction"""
    FIELD_LIST = [
        'transactionId',
        'caseIds',
        'transactionWindowSize'
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
    @classmethod
    def creatNewTransactionId(cls):
        return "{}-{}".format( uuid.uuid4(), datetime.now().isoformat())

    @classmethod
    def createTransaction(cls, winSize, caseIds):

        transactionId = cls.creatNewTransactionId()
        logger.info("Transaction id : {} dispatched.".format(transactionId))

        transactionTable = DBManager.table("Transactions")
        transactionTable.put_item(
            Item = {
                'transactionId' : transactionId,
                'caseIDs' : caseIds,
                'transactionWindowSize' : winSize
            }
        )
        logger.info("Added transaction: {} to database".format(transactionId))

        return transactionId