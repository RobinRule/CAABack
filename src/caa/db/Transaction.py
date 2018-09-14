
from .DBManager import DBManager
from .BaseDataClass import BaseDataClass
from .Case import Case

from datetime import datetime
from dateutil.parser import parse as timeParse
from boto3.dynamodb.conditions import Key, Attr
import logging
import uuid

logger = logging.getLogger(__name__)

class Transaction(BaseDataClass):
    """docstring for Transaction"""
    
    def __init__(self, jsonObj=None):
        super(Transaction, self).__init__(
            [
                'transactionId',
                'caseIds',
                'transactionWindowSize'
            ],
            jsonObj
        )

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
class ClassName(object):
    """docstring for ClassName"""
    def __init__(self, arg):
        super(ClassName, self).__init__()
        self.arg = arg
        
