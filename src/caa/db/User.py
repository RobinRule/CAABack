
from .DBManager import DBManager
from .BaseDataClass import BaseDataClass
import boto3
import logging
import random
import string

logger = logging.getLogger(__name__)

from global_var import CFG

END_POINT = CFG.get('cognito', 'endpoint')
POOL_ID = CFG.get('cognito', 'pool_id')
CLIENT_ID = CFG.get('cognito', 'client_id')

params = {}
params['aws_access_key_id'] = CFG.get('aws_credential', 'aws_access_key_id')
params['aws_secret_access_key'] = CFG.get('aws_credential', 'aws_secret_access_key')

COGNITO_CLIENT = boto3.client('cognito-idp', **params)

class CognitoUser:
    
    # Throwout exception if the token being used is invalid
    @classmethod
    def getUser(cls, token):
        user = COGNITO_CLIENT.get_user(
            AccessToken=token
        )
        return user['Username']

    @classmethod
    def genTempPassword(cls):
        return ''.join(random.choices(string.ascii_uppercase, k=3))\
                + ''.join(random.choices(string.digits, k=4))

    @classmethod
    def addUser(cls, newUserEmail):
        params = {
            "UserPoolId" : POOL_ID,
            "Username" : newUserEmail,
            "UserAttributes": [
                {
                    'Name': 'email',
                    'Value': newUserEmail
                },
            ],
            "TemporaryPassword" : cls.genTempPassword(),
            "ForceAliasCreation" : True|False,
            "MessageAction" : 'RESEND',
            "DesiredDeliveryMediums" : [
                'EMAIL'
            ]
        }
        logger.info("Creating user : {userDetail}".format(userDetail=params))
        try:
            resp = COGNITO_CLIENT.admin_create_user(**params)
        except Exception as e:
            logger.exception("User creation failed.")
            return False
        return True
        