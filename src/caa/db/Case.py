
from .DBManager import DBManager
from .BaseDataClass import BaseDataClass
from datetime import datetime
from dateutil.parser import parse as timeParse
from boto3.dynamodb.conditions import Key, Attr
import logging


logger = logging.getLogger(__name__)

class Case(BaseDataClass):
    """Case object"""
    MAX_ID = None
    KEYS = ['caseId', 'userId']
    def __init__(self, jsonObj=None):
        super(Case, self).__init__(
            [
                ['userId', 'caseId'], #KEYS
                'nameFirst',
                'nameLast',
                'contact',
                'statusId',
                'creatTime',
                'closeTime' 
            ],
            jsonObj
        )