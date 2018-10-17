import boto3
from db.User import CognitoUser, User
from db.Transaction import Transaction

from .TransactionBusiness import TransactionBusiness
import logging

logger = logging.getLogger(__name__)

from global_var import CFG
from global_var import Errors

class UserBusiness(object):
    """docstring for UserBusiness"""
    @classmethod
    def addUser(cls, requesterId, user):
        status, err = User.addUser(requesterId, user)
        return {
            "status" :  status,
            "error" : err
        }

    @classmethod
    def getUser(cls, requesterId, userId):
        if User.isSuperior(requesterId, userId):
            status, user = User.getItem(userId)
            if not status:
                return { "error" : "Error when querying user: {}".format(userId)}
            return { "content" :  user }
        else:
            return { "error" : str(Errors.ErrorNotEnoughPermisson)}

    @classmethod
    def updateUser(cls, userJson):
        raise NotImplementedError()
        return { "error" : str(Errors.ErrorNoSuchId) }

    # check whether an token is valid. returns user_id for token owner
    @classmethod
    def checkToken(cls, token):
        return CognitoUser.getUserByToken(token)['userId']

    @classmethod
    def createTransaction(cls, requesterId, targetUserId, winSize, specs):
        # step 1: check does requesterId have enough permission
        if not User.isSuperior(requesterId, targetUserId):
            return { "error" : str(Errors.ErrorNotEnoughPermisson)}

        # step 2: get all of target user's inferior user
        status, userIds = User.getAllInferiors(targetUserId)
        users = User.getItemsByIds(userIds)
        # Todo: filter out user base on specs
        if len(userIds) <= winSize:
            return { "users" : users }
        # step 3: create transaction
        transacJson = {
            "winSize" : winSize,
            "userId" : requesterId,
            "itemIds" : [{'userId' : user['userId'] } for user in users[winSize:]],
            'timeToLive' : 10
        }
        transacId = Transaction.addItem(Transaction(transacJson))

        # Step 4: return first page of cases
        return {
            "transaction_id" : transacId,
            "users" : users[:winSize]
        }

    @classmethod
    def getUsersByTransacId(cls, requesterId, transactionId):
        return TransactionBusiness.consumeTransaction(requesterId, transactionId, User())

