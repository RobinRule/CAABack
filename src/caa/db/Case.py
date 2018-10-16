
from .DBManager import DBManager
from .BaseDataClass import BaseDataClass
from datetime import datetime
import logging


logger = logging.getLogger(__name__)

class Case(BaseDataClass):
    """Case object"""
    def __init__(self, jsonObj=None):
        super(Case, self).__init__(
            [
                ('caseId', str), #Key
                ('userId', str), 
                ('nameFirst', str ),
                ('nameLast', str ),
                ('contact', str ),
                ('statusId', str),
                ('createTime', datetime),
                ('closeTime', datetime)
            ],
            jsonObj
        )