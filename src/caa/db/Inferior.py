
from .DBManager import DBManager
from .BaseDataClass import BaseDataClass
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr
import logging


logger = logging.getLogger(__name__)

class Inferior(BaseDataClass):
    """Case object"""
    def __init__(self, jsonObj=None):
        super(Inferior, self).__init__(
            [
                ('userId', str), #Key
                ('inferiors', list)
            ],
            jsonObj
        )