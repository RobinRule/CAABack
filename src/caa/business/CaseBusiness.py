
from db.Case import Case

class CaseBusiness(object):
	"""docstring for CaseBusiness"""
	@classmethod
	def getCase(cls, caseId):
		return Case.getCase(caseId)

	@classmethod
	def delCase(cls, caseId):
		pass

	@classmethod
	def addCase(cls, case):
		pass

	@classmethod
	def updateCase(cls, case):
		pass