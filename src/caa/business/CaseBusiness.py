
from db.Case import Case
from .UserBusiness import UserBusiness
from db.Transaction import Transaction
from .TransactionBusiness import TransactionBusiness
from .UserBusiness import UserBusiness
from global_var import Errors
import logging

logger = logging.getLogger(__name__)
class CaseBusiness(object):
	"""docstring for CaseBusiness"""
	@classmethod
	def getCase(cls, userId, caseId):
		item = Case( {'caseId' : caseId, 'userId' : userId} )
		item = Case.getItem(item)
		if item is None:
			return { "error" : str(Errors.ErrorNoSuchId) }
		return { "content" : item }

	@classmethod
	def delCase(cls, userId, caseId):
		item = Case( {'caseId' : caseId, 'userId' : userId} )
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
	def createTransaction(cls, callerToken, userId, winSize, specs = None):
		# Step 1: check this does this client has priviledges to get data fo this userId
		callerUserId = UserBusiness.check_token(callerToken)
		priviledge = UserBusiness.checkPriviledges(callerUserId, userId)
		if "read" not in priviledge:
			return { "error" : "Caller doesn't have enough priviledge to perform this operation" }

		# Step 2: perfom query
		specs = [{
			"attr_name" : "userId",
			"attr_val" : userId
		}] + specs
		cases = Case.getItemsByQuery(specs, Case())
		if type(cases) is Errors:
			return { "error" : str(cases) }
		# if winSize is bigger than number of cases, return all at once
		if len(cases) <= winSize:
			return { "cases" : cases }

		# Step 3: create Transaction
		transacJson = {
		    "winSize" : winSize,
		    "userId" : callerUserId,
			"itemIds" : [{'caseId' : case['caseId'] } for case in cases[winSize:]],
			'timeToLive' : 10
		}
		transacId = Transaction.addItem(Transaction(transacJson))

		# Step 4: return first page of cases
		return {
			"transaction_id" : transacId,
			"cases" : cases[:winSize]
		}

	@classmethod
	def getCasesByTransacId(cls, callerToken, transactionId):
		# first authorize whether this caller is the same as the 
		return TransactionBusiness.consumeTransaction(callerToken, transactionId, Case())