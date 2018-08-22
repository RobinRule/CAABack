
from db.Case import Case

class CaseBusiness(object):
	"""docstring for CaseBusiness"""
	@classmethod
	def getCase(cls, caseId):
		# return { "hahah":123}
		return Case.getCase(caseId)

	@classmethod
	def delCase(cls, caseId):
		pass

	@classmethod
	def addCase(cls, case):

		return Case.addCase(Case([None, case["usrId"], case["custId"], case["status"], case["creatTime"], None]))

	@classmethod
	def updateCase(cls, case):
		pass