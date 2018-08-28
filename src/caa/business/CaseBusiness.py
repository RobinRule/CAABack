
from db.Case import Case

class CaseBusiness(object):
	"""docstring for CaseBusiness"""
	@classmethod
	def getCase(cls, userId, caseId):
		return Case.getCase(int(userId), int(caseId))

	@classmethod
	def delCase(cls, userId, caseId):
		return Case.delCase(int(userId), int(caseId))

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
	def updateCase(cls, caseJson):
		caseObj = Case()
		for key in caseJson:
			if caseJson[key]:
				setattr(caseObj, key, caseJson[key])
		return Case.updateCase(caseObj)

	# @classmethod
	# def getCaseList(cls, usrId):
	# 	return Case.getCaseList(usrId)