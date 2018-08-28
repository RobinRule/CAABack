
from db.Case import Case

class CaseBusiness(object):
	"""docstring for CaseBusiness"""
	@classmethod
	def getCase(cls, userId, caseId):
		return Case.getCase(int(userId), int(caseId))

	@classmethod
	def delCase(cls, caseId):
		return Case.delCase(int(caseId))

	@classmethod
	def addCase(cls, jsonCase):
		return Case.addCase(
			Case([None, 
				jsonCase["userId"], 
				jsonCase["statusId"], 
				jsonCase["createTime"]
				])
			)

	@classmethod
	def updateCase(cls, case):
		case = Case()
		for key in case:
			if case[key]:
				setattr(case, key, case[key])
		return Case.updateCase(case)

	# @classmethod
	# def getCaseList(cls, usrId):
	# 	return Case.getCaseList(usrId)