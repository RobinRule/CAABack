from db.User import User
import logging

logger = logging.getLogger(__name__)

class UserBusiness(object):
	"""docstring for UserBusiness"""
	# @classmethod
	# def get():
	# 	pass
	
	@classmethod
	def checkPriviledges(cls, userId1, userId2):
		raise NotImplementedError("checkPriviledges")
		#check userId1's priviledge towars userId2
		return ["read"]