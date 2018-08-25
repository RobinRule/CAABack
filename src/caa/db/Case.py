
from DBManager import DBManager
from datetime import datetime
from dateutil.parser import parse as timeParse
import logging


logger = logging.getLogger(__name__)

class Case(object):
    """Case object"""
    MAX_ID = None

    def __init__(self, dbRecord=None):
        if dbRecord:
            self.caseId = dbRecord[0]
            self.usrId = dbRecord[1]
            self.custId = dbRecord[2]
            self.status = dbRecord[3]
            self.creatTime = timeParse(dbRecord[4])
            self.closeTime = timeParse(dbRecord[5]) if dbRecord[5] else dbRecord[5]
        else:
            self.caseId = None
            self.usrId = None
            self.custId = None
            self.status = None
            self.creatTime = None
            self.closeTime = None
    
    # add a new case to database, return a Case Id
    @classmethod
    def addCase(cls, case):

        # get maxId from db after setup
        # if  Case.MAX_ID is None:
        #     cursor = DBManager.cursor()
        #     cursor.execute("SELECT MAX(caseId) FROM CASES;")
        #     result = cursor.fetchone()
        #     Case.MAX_ID = result[0] if not (result[0] is None) else -1
        Case.MAX_ID = 100
        newCaseId = Case.MAX_ID + 1

        logger.info("Allocated id is :{}".format(newCaseId))

        DBManager.table("Cases").put_item(
            Item={
                'caseId': newCaseId,
                'usrId': case.usrId,
                'custId': case.custId,
                'status' : case.status,
                'creatTime' : case.creatTime.isoformat(),
            }

        )
        # con = DBManager.connection()
        # query = "INSERT INTO CASES\
        # ( caseId, usrId, custId, status, creatTime)\
        # VALUES ({caseId}, {usrId}, {custId}, '{status}', '{creatTime}');".\
        # format(
        #     caseId = newCaseId, usrId = case.usrId, custId = case.custId,
        #     status = case.status, creatTime = case.creatTime)
        # logger.info("Executing query:{}".format(query))
        # con.execute(query)
        # Case.MAX_ID += 1
        return newCaseId


    # remove a case from database by Id
    @classmethod
    def delCase(cls, caseId):
        query = "DELETE FROM CASES WHERE caseId == {}".format(int(caseId))
        conn = DBManager.connection()
        conn.execute(query)

    @classmethod
    def updateCaseStatus(cls, caseId, caseStatus):

        response = caseTable.update_item(
            Key={
                'caseId': caseId,
            },
            UpdateExpression = "set caseStatus = :p ",
            ExpressionAttributeValues = {
                ':p': caseStatus,
            }
        )
        # query = "UPDATE CASES\
        #     SET status='{}' WHERE caseId={}".format(str(caseStatus), int(caseId))
        # DBManager.connection().execute(query)

    # get a case by caseId
    @classmethod
    def getCase(cls, caseId):
        response = DBManager.table("Cases").get_item(
            Key={
                'caseId': int(caseId),
            }
        )

        item = response['Item']
        print("GetCase succeeded:")
        print(item['usrId'])
        print item
        return item
        # cursor = DBManager.cursor()
        # query = "SELECT * FROM CASES where caseID={};".format(caseId)
        # cursor.execute(query)
        # caseRecord = cursor.fetchone()
        # logger.info("Returning caseRecord:{}".format(caseRecord))
        # if caseRecord is None:
        #     return None
        # return Case( dbRecord = caseRecord )s

    # get caseList by usrId, default return all case belongs to the usrId
    @classmethod
    def getCaseList(cls, usrId, limit):
        response = DBManager.table("Cases").scan(
            FilterExpression=Attr('usrId').eq(usrId)
        )
        print("GetCase succeeded:")
        for i in response['Items']:
            print(i['caseId'], ":", i['usrId'])

        return response['Items']

    def __repr__(self):
        return "{{ caseId : {}, usrId : {}, custId : {}, status : {}, creatTime : {}, closeTime : {}}}".\
        format(self.caseId,
            self.usrId,
            self.custId,
            self.status,
            self.creatTime,
            self.closeTime)

    def __eq__(self, obj):
        return self.caseId == obj.caseId and\
            self.usrId == obj.usrId and\
            self.custId == obj.custId and\
            self.status == obj.status and\
            self.creatTime == obj.creatTime and\
            self.closeTime == obj.closeTime

