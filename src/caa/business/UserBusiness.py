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
        userId = user['username']

        # add this user, automatically sent out invitation
        if not CognitoUser.addUser(user['username'], user['email']):
            return { "error" : "Falied to add user."}

        # add invitee as invitor's Inferior
        callerId = cls.checkToken(token)
    
        inferiorObj = Inferior({"userId" : callerId})        
        callerInferios = Inferior.getItem(inferiorObj)
        if type(callerInferios) is Errors:
            Inferior.addItem(Inferior({"inferiors" : [ userId]}), lambda : callerId)
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
    def getUser(cls, token, userId):
        pass

    # check whether an token is valid. returns user_id for token owner
    @classmethod
    def checkToken(cls, token):
        return CognitoUser.getUser(token)