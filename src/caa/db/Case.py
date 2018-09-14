
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
    def __init__(self, dbRecord=None, jsonObj=None):
        super(Case, self).__init__(
            [
                ['caseId', 'userId'], #KEYS
                'nameFirst',
                'nameLast',
                'contact',
                'statusId',
                'creatTime',
                'closeTime' 
            ],
            jsonObj
        )

    # remove a case from database by Id
    @classmethod
    def delCase(cls, userId, caseId):
        caseTable = DBManager.table("Cases")
        try:
            caseTable.delete_item(
                Key={
                    'caseId' : caseId,
                    'userId' : userId
                }
            )
        except Exception as e:
            logger.exception("Failed to delete case : {}".format(caseId))
            return False
        else:
            logger.debug("Deleted case : {}".format(caseId))
            return True

    # update a case
    @classmethod
    def updateCase(cls, case):
        caseTable = DBManager.table('Cases')
        exp = "set "
        valMap = {}
        for key in (set(case.getAttrs()) - set(case.getKeys())):
            attrVal = getattr(case, key)
            if attrVal:
                exp += " {keyName} = :{keyName},".format(keyName=key)
                valMap[":{}".format(key)] = DBManager.dataToStr(attrVal)
        try:
            resp = caseTable.update_item(
                Key={
                    'caseId': case.caseId,
                    'userId': case.userId
                },
                UpdateExpression = exp[:-1],
                ExpressionAttributeValues = valMap,
                ReturnValues="UPDATED_NEW"
            )
        except Exception as e:
            logger.exception("Failed to update case: {}".format(case.caseId))
            return False
        else:
            return True

    # get a case by caseId
    @classmethod
    def getCase(cls, userId, caseId):
        caseTable = DBManager.table("Cases")
        response = caseTable.get_item(
            Key={
                'caseId': int(caseId),
                'userId': int(userId)
            }
        )

        item = DBManager.toJsonData(response['Item'])
        logger.debug("Returning case: {}".format(item['caseId']))
        return item

    # get all cases from this user
    def getCases(cls, userId):
        pass

    # get caseList by usrId, default return all case belongs to the usrId
    @classmethod
    def getCaseList(cls, usrId, specs):
        response = DBManager.table("Cases").query(
              KeyConditionExpression=Key('userId').eq(usrId)
        )

        for spec in specs:
            pass

        logger.info("GetCaseList succeeded for user:{}".format(usrId))
        return DBManager.toJsonData(response['Items'])