
from .DBManager import DBManager
from .BaseDataClass import BaseDataClass
from .Case import Case

from datetime import datetime
from dateutil.parser import parse as timeParse
from boto3.dynamodb.conditions import Key, Attr
import logging
import uuid

logger = logging.getLogger(__name__)

class Car(BaseDataClass):
    """docstring for Transaction"""
    
    def __init__(self, jsonObj=None):
        super(Car, self).__init__(
            [
                ( 'carId', str),
                ( 'frontPic', str),
                ( 'backPic', str),
                ( 'leftPic', str),
                ( 'rightPic', str),
                ( 'insidePic', str),
                ( 'otherPics', list)
            ],
            jsonObj
        )

    @classmethod
    def newItemId(cls, item):
        return uuid.uuid4()

        
