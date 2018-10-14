import boto3
from db.User import CognitoUser
from db.Inferior import Inferior
import logging

logger = logging.getLogger(__name__)

# COGNITO_CLIENT = boto3.client('cognito-identity')
from global_var import CFG
from global_var import Errors

class UserBusiness(object):
    """docstring for UserBusiness"""
    @classmethod
    def addUser(cls, token, user):
        userId = user['email']

        # add this user, automatically sent out invitation
        CognitoUser.addUser(userId)

        # add invitee as invitor's Inferior
        callerId = check_token(token)
        callerInferios = Inferior.getItem(Inferior({"userId" : callerId}))
        if type(callerInferios) is Errors:
            Inferior.addItem({"userId" : callerId, "inferiors" : [ userId]})
        else:
            callerInferios['inferiors'].append(user)
            Inferior.updateItem(callerInferios)
        return { "status" : True }
    
    @classmethod
    def checkPriviledges(cls, userId1, userId2):
        # raise NotImplementedError("checkPriviledges")
        #check userId1's priviledge towars userId2
        return ["read"]

    @classmethod
    def getUserByToken(cls, token):
        pass

    # check whether an token is valid. returns user_id for token owner
    @classmethod
    def check_token(cls, token):
        return CognitoUser.getUser(token)