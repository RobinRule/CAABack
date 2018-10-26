
from .DBManager import DBManager
from .BaseDataClass import BaseDataClass

import boto3
import logging
import random
import string
import copy

logger = logging.getLogger(__name__)

from global_var import CFG

END_POINT = CFG.get('cognito', 'endpoint')
POOL_ID = CFG.get('cognito', 'pool_id')
CLIENT_ID = CFG.get('cognito', 'client_id')

params = {}
params['aws_access_key_id'] = CFG.get('aws_credential', 'aws_access_key_id')
params['aws_secret_access_key'] = CFG.get('aws_credential', 'aws_secret_access_key')

logger.info("Creating cognito client with params:{}".format(params))
COGNITO_CLIENT = boto3.client('cognito-idp', **params)

class DBUser(BaseDataClass):
    """Inferior object"""
    def __init__(self, jsonObj=None):
        super(DBUser, self).__init__(
            [
                ('userId', str), #Key
                ('inferiors', list),
                ('superior', str)
            ],
            jsonObj
        )

class CognitoUser:
    @classmethod
    def convertToUser(cls, cognitoUser):
        user = copy.deepcopy(cognitoUser)
        del user['ResponseMetadata']
        del user['UserAttributes']
        del user['Username']
        user['userId'] = cognitoUser['Username']
        for userAttribute in cognitoUser["UserAttributes"]:
            user[userAttribute['Name']] = userAttribute['Value']
        return user

    # Throwout exception if the token being used is invalid
    @classmethod
    def getUserByToken(cls, token):
        user = COGNITO_CLIENT.get_user(
            AccessToken=token
        )
        return cls.convertToUser(user)

    @classmethod
    def getUserByUsername(cls, username):
        user = COGNITO_CLIENT.admin_get_user(
            Username=username,
            UserPoolId=POOL_ID
        )
        return cls.convertToUser(user)


    @classmethod
    def genTempPassword(cls):
        return ''.join(random.choices(string.ascii_uppercase, k=3))\
                + ''.join(random.choices(string.ascii_lowercase, k=2))\
                + '@'\
                + ''.join(random.choices(string.digits, k=4))

    @classmethod
    def addUser(cls, username, newUserEmail):
        params = {
            "UserPoolId" : POOL_ID,
            "Username" : username,
            "UserAttributes": [
                {
                    'Name': 'email',
                    'Value': newUserEmail
                },
            ],
            "TemporaryPassword" : cls.genTempPassword(),
            "ForceAliasCreation" : False,
            "DesiredDeliveryMediums" : [
                'EMAIL'
            ]
        }
        logger.info("Creating user : {userDetail}".format(userDetail=params))
        try:
            resp = COGNITO_CLIENT.admin_create_user(**params)
        except COGNITO_CLIENT.exceptions.UsernameExistsException:
            logger.error("Username already existed.")
            return False, "Username already existed."
        except Exception:
            logger.exception("User creation failed.")
            return False, "Unknown error occured."
        return True, None

class User:
    @classmethod
    def getItem(cls, userId):
        # get cognito user attr
        user = CognitoUser.getUserByUsername(userId)
        # get inferiors
        _, inferiors = DBUser.getItem(DBUser({"userId":userId}))
        user["inferiors"] = inferiors.get("inferiors", [])
        return True, user

    @classmethod
    def addUser(cls, requesterId, user):
        userId = user['username']

        # add this user, automatically sent out invitation
        status, err = CognitoUser.addUser(user['username'], user['email'])
        if not status:
            return False, err

        # add invitee as invitor's Inferior
        User.addBelongship(requesterId, userId)
        return True, None

    @classmethod
    def getItemsByIds(cls, userIds, item = None):
        return [ cls.getItem(userId['userId'])[1] for userId in userIds ]

    @classmethod
    def addBelongship(cls, superiorId, inferiorId):
        dbUserObj = DBUser({"userId" : superiorId})
        status, inferios = DBUser.getItem(dbUserObj)
        if not status:
            DBUser.addItem(DBUser({"inferiors" : [ inferiorId]}), lambda : superiorId)
        else:
            inferios['inferiors'].append(inferiorId)
            DBUser.updateItem(DBUser(inferios))

        dbUserObj = DBUser({"userId" : inferiorId})
        status, superior = DBUser.getItem(dbUserObj)
        if not status:
            DBUser.addItem(DBUser({"superior" : superiorId}), lambda : inferiorId)
        else:
            inferios['superior'] = superiorId
            DBUser.updateItem(DBUser(superior))

    @classmethod
    def deleteBelongship(cls, superior, inferior):
        raise NotImplementedError()

    # returns True if userId1 is userId2's superior
    @classmethod
    def isSuperior(cls, userId1, userId2):
        if userId1 == userId2:
            return True
        logger.info("Checking for {} {}".format(userId1, userId2))
        isRoot = False
        curUser = userId2
        superiors = set()
        # gather all superiors of user2
        while True:
            status, dbUserJson = DBUser.getItem(DBUser({"userId":curUser}))
            if not status:
                logger.error("Error, corruptued database.")
                raise Exception("Error, corruptued database. No record for user:{}".format(curUser))
            superior = dbUserJson.get("superior", None)
            isRoot = superior is None
            if not isRoot:
                superiors.add(superior)
                curUser = superior
            else:
                break
        return userId1 in superiors

    @classmethod
    def getAllInferiors(cls, userId):
        status, dbUserJson = DBUser.getItem(DBUser({"userId":userId}))
        if not status:
            return False, "NoSuchUser"
        return True, dbUserJson["inferiors"]
