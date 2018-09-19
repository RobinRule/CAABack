
from db.Case import Case
from .UserBusiness import UserBusiness
from .TransactionBusiness import TransactionBusiness
from global_var import Errors
import logging

logger = logging.getLogger(__name__)
class CaseBusiness(object):
	"""docstring for CaseBusiness"""
	@classmethod
	def getCase(cls, userId, caseId):
		item = Case( {'caseId' : int(caseId), 'userId' : int(userId)} )
		item = Case.getItem(item)
		if item is None:
			return { "error" : str(Errors.ErrorNoSuchId) }
		return { "content" : item }

	@classmethod
	def delCase(cls, userId, caseId):
		item = Case( {'caseId' : int(caseId), 'userId' : int(userId)} )
		return{ "result" : Case.deleteItem(item) }

	@classmethod
	def addCase(cls, jsonCase):
		newCaseId = Case.addItem(
			Case(jsonCase)
			)
		if newCaseId is None:
			return { "error" : str(Errors.ErrorRequestIllFormated)}
		return{ "content" : newCaseId }

	@classmethod
	def updateCase(cls, caseJson):
		caseObj = Case(caseJson)
		if Case.updateItem(caseObj):
			return { "content" : Case.getItem(caseObj) }
		return { "error" : str(Errors.ErrorNoSuchId) }


	@classmethod
	def createTransaction(cls, callerUserId, userId, specs = None):
		# Step 1: check this does this client has priviledges to get data fo this userId
		priviledge = UserBusiness.checkPriviledges(callerUserId, userId)
		if "read" not in priviledge:
			return { "error" : "Caller doesn't have enough priviledge to perform this operation" }

		# Step 2: perfom query
		specs = [{
			"attr_name" : "userId",
			"attr_val" : userId
		}] + specs
		cases = Case.getItems(specs)

		# Step 3: create Transaction
		transacJson = {
		    "transactionWindowSize" : winsize,
			"caseIds" : [{'userId' : case['userId'], 'caseId' : case['caseId'] } for case in cases[winSize:]]
		}
		transacId = TransactionBusiness.addItem(Transaction(transacJson))

		# Step 4: return first page of cases
		return {
			"transaction_id" : transacId,
			"cases" : cases[:winSize]
		}

	@classmethod
	def get_cases_by_transaction():
		# first authorize whether this 
		pass