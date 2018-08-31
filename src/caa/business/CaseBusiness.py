
from db.Case import Case
import logging

logger = logging.getLogger(__name__)
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
		newCaseId = Case.addCase(
			Case([None,
				jsonCase["userId"],
				None,
				None,
				None,
				jsonCase["statusId"],
				"20180202",
				None
				])
			)
		return newCaseId

	@classmethod
	def updateCase(cls, caseJson):
		caseObj = Case()
		for key in caseJson:
			if caseJson[key]:
				setattr(caseObj, key, caseJson[key])
		return Case.updateCase(caseObj)

	@classmethod
	def getCaseList(cls, userId, specs = None):
		return Case.getCaseList(int(userId), specs)