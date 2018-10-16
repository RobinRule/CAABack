
from .DBManager import DBManager
from .BaseDataClass import BaseDataClass
from datetime import datetime
import logging


logger = logging.getLogger(__name__)

class Inferior(BaseDataClass):
    """Inferior object"""
    def __init__(self, jsonObj=None):
        super(Inferior, self).__init__(
            [
                ('userId', str), #Key
                ('inferiors', list)
            ],
            jsonObj
        )