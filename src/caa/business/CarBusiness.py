import boto3
from db.Car import Car
from db.Transaction import Transaction

from .TransactionBusiness import TransactionBusiness
import logging

logger = logging.getLogger(__name__)

from global_var import CFG
from global_var import Errors

class CarrBusiness(object):
    """docstring for CarBusiness"""
    @classmethod
    def addCar(cls, requesterId, user):
        status, err = Car.addCar(requesterId, user)
        return {
            "status" :  status,
            "error" : err
        }

    @classmethod
    def getCar(cls, requesterId, userId):
        if Car.isSuperior(requesterId, userId):
            status, user = Car.getItem(userId)
            if not status:
                return { "error" : "Error when querying user: {}".format(userId)}
            return { "content" :  user }
        else:
            return { "error" : str(Errors.ErrorNotEnoughPermisson)}

    @classmethod
    def updateCar(cls, userJson):
        raise NotImplementedError()
        return { "error" : str(Errors.ErrorNoSuchId) }

    # @classmethod
    # def createTransaction(cls, requesterId, targetCarId, winSize):
    #     # step 1: check does requesterId have enough permission
    #     if not Car.isSuperior(requesterId, targetCarId):
    #         return { "error" : str(Errors.ErrorNotEnoughPermisson)}

    #     # step 2: get all of target user's inferior user
    #     status, userIds = Car.getAllInferiors(targetCarId)
    #     users = [Car.getItem(userId)[1] for userId in userIds]

    #     if len(userIds) <= winSize:
    #         return { "users" : users }
    #     # step 3: create transaction
    #     transacJson = {
    #         "winSize" : winSize,
    #         "userId" : requesterId,
    #         "itemIds" : [{'userId' : user['userId'] } for user in users[winSize:]],
    #         'timeToLive' : 10
    #     }
    #     transacId = Transaction.addItem(Transaction(transacJson))

    #     # Step 4: return first page of cases
    #     return {
    #         "transaction_id" : transacId,
    #         "users" : users[:winSize]
    #     }

    # @classmethod
    # def getCarsByTransacId(cls, requesterId, transactionId):
    #     return TransactionBusiness.consumeTransaction(requesterId, transactionId, Car())

