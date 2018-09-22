
from .DBManager import DBManager
from .BaseDataClass import BaseDataClass
import logging


logger = logging.getLogger(__name__)

class User(BaseDataClass):
    """User object"""
    def __init__(self, dbRecord=None, jsonObj=None):
        super(User, self).__init__(
            [
                [("userId", int) ], #KEYS
                ('nameFirst', str),
                ('nameLast', str),
                ('contact' , str)
            ],
            jsonObj
        )