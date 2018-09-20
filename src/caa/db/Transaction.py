
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
                [ ('transactionId', str)],
                ( 'itemIds', list )
                ( 'transactionWindowSize', int)
            ],
            jsonObj
        )

    @classmethod
    def creatNewTransactionId(cls):
        return "{}-{}".format( uuid.uuid4(), datetime.now().isoformat())

        
