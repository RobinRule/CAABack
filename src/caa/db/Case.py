
from .DBManager import DBManager
from .BaseDataClass import BaseDataClass
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr
import logging


logger = logging.getLogger(__name__)

class Case(BaseDataClass):
    """Case object"""
    def __init__(self, jsonObj=None):
        super(Case, self).__init__(
            [
                [('userId', int), ('caseId', int)], #KEYS
                ('nameFirst', str ),
                ('nameLast', str ),
                ('contact', str ),
                ('statusId', int),
                ('creatTime', datetime),
                ('closeTime', datetime)
            ],
            jsonObj
        )