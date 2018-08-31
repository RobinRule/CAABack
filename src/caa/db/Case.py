
from .DBManager import DBManager
from datetime import datetime
from dateutil.parser import parse as timeParse
from boto3.dynamodb.conditions import Key, Attr
import logging


logger = logging.getLogger(__name__)

class Case(object):
    """Case object"""
    MAX_ID = None
    FIELD_LIST = [
        'caseId',
        'userId',
        'nameFirst',
        'nameLast',
        'contact',
        'statusId',
        'creatTime',
        'closeTime' 
    ]
    KEYS = ['caseId', 'userId']
    def __init__(self, dbRecord=None):
        if dbRecord:
            self.caseId = dbRecord[0]
            self.userId = dbRecord[1]
            self.nameFirst = dbRecord[2]
            self.nameLast = dbRecord[3]
            self.contact = dbRecord[4]
            self.statusId  = dbRecord[5]
            self.creatTime = timeParse(dbRecord[6])
            self.closeTime = timeParse(dbRecord[7]) if dbRecord[7] else dbRecord[7]
        else:
            for attr in Case.FIELD_LIST:
                setattr(self, attr, None)
    
    # add a new case to database, return a Case Id
    @classmethod
    def addCase(cls, case):
        caseTable = DBManager.table("Cases")

        response = caseTable.query(
              Limit = 1,
              ScanIndexForward = False,
              KeyConditionExpression=Key('userId').eq(case.userId) & Key('caseId').gt(0)
        )
        newCaseId = 1
        if len(response['Items']):
            largestCaseId = response['Items'][0]['caseId']
            newCaseId = int(largestCaseId) + 1
        # TODO: base on the input to decide what to add
        logger.info("Allocated id is :{}".format(newCaseId))
        caseTable.put_item(
            Item={
                'caseId': newCaseId,
                'userId': case.userId,
                # 'custId': case.custId,
                'statusId' : case.statusId,
                'creatTime' : case.creatTime.isoformat(),
            }
        )
        logger.info("Added case: {} to database".format(newCaseId))
        # return 1
        return newCaseId


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
        for key in (set(cls.FIELD_LIST) - set(cls.KEYS)):
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


    # get caseList by usrId, default return all case belongs to the usrId
    @classmethod
    def getCaseList(cls, usrId, specs):
        response = DBManager.table("Cases").query(
              KeyConditionExpression=Key('userId').eq(usrId)
        )
        logger.info("GetCaseList succeeded for user:{}".format(usrId))
        return DBManager.toJsonData(response['Items'])

    def __repr__(self):
        return "{{ caseId : {}, usrId : {}, custId : {}, status : {}, creatTime : {}, closeTime : {}}}".\
        format(self.caseId,
            self.usrId,
            self.custId,
            self.statusId ,
            self.creatTime,
            self.closeTime)

    def __eq__(self, obj):
        return self.caseId == obj.caseId and\
            self.usrId == obj.usrId and\
            self.custId == obj.custId and\
            self.statusId  == obj.statusId and\
            self.creatTime == obj.creatTime and\
            self.closeTime == obj.closeTime

