
from .DBManager import DBManager
from .BaseDataClass import BaseDataClass
from .Case import Case

from datetime import datetime
from dateutil.parser import parse as timeParse
from boto3.dynamodb.conditions import Key, Attr
import logging
import uuid

logger = logging.getLogger(__name__)

class Resource(BaseDataClass):
    """docstring for Transaction"""
    
    def __init__(self, jsonObj=None):
        super(Resource, self).__init__(
            [
                ( 'resourceId', str),
                ( 'uploaded', bool)
            ],
            jsonObj
        )

    @classmethod
    def newItemId(cls, item):
        return "{}-{}".format( uuid.uuid4(), datetime.now().isoformat())

        
