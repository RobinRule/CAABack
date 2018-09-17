
from db.Case import Case
from .UserBusiness import UserBusiness
from .TransactionBusiness import TransactionBusiness
import logging

logger = logging.getLogger(__name__)
class CaseBusiness(object):
	"""docstring for CaseBusiness"""
	@classmethod
	def getCase(cls, userId, caseId):
		item = Case( {'caseId' : int(caseId), 'userId' : int(userId)} )
		return Case.getItem(item)

	@classmethod
	def delCase(cls, userId, caseId):
		item = Case( {'caseId' : int(caseId), 'userId' : int(userId)} )
		return Case.deleteItem(item)

	@classmethod
	def addCase(cls, jsonCase):
		newCaseId = Case.addItem(
			Case(jsonCase)
			)
		return newCaseId

	@classmethod
	def updateCase(cls, caseJson):
		caseObj = Case(caseJson)
		return Case.updateCase(caseObj)

	@classmethod
	def createTransaction(cls, callerUserId, userId, specs = None):
		# Step 1: check this does this client has priviledges to get data fo this userId
		priviledge = UserBusiness.checkPriviledges(callerUserId, userId)
		if "read" not in priviledge:
			return { "error" : "Caller doesn't have enough priviledge to perform this operation" }

		# Step 2: perfom query
		caseIds = Case.getCaseList(int(userId), specs)

		# Step 3: create Transaction
		transacId = TransactionBusiness.createTransaction( winsize, caseIds[winSize:] )

		# Step 4: get first page of cases
		cases = Case.getCasesByIds(caseIds[:winSize])
		return {
			"transaction_id" : transacId,
			"cases" : cases
		}

	@classmethod
	def get_cases_by_transaction():
		# first authorize whether this 
		pass