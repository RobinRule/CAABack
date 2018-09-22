from db.Transaction import Transaction
from global_var import Errors


import logging
logger = logging.getLogger(__name__)

class TransactionBusiness(object):
	"""docstring for TransactionBusiness"""
	
	@classmethod
	def consumeTransaction(cls, callerToken, transactionId, item):
		callerUserId = callerToken #TODO: convert this to userId

		oldTransactionJson = Transaction.getItem(Transaction({'transactionId' : transactionId}))
		if type(oldTransactionJson) is Errors:
			return { "error" : str(oldTransactionJson) }
		
		# Step 1: verify that callerId is correct
		if oldTransactionJson['userId'] != callerUserId:
			return { "error" : str(Errors.NotAuthoriedOperation)}

		# Step 2 : populate ids into items
		winSize = oldTransactionJson['winSize']
		itemIds = oldTransactionJson['itemIds']

		queryIds = itemIds if len(itemIds) <= winSize else itemIds[0:winSize]
		returnItems = item.getItemsByIds(queryIds, item)

		# Step 3: Generate a new trasaction
		newTransactionId = None
		if len(returnItems) > winSize:
			newTransactionJson = {
				'itemIds' : itemIds[winSize:],
				'winSize' : winSize,
				'timeToLive' : 10
			}
			newTransactionId = Transaction.addItem(Transaction(newTransactionJson))

		# Step 4: delete old transaction
		Transaction.deleteItem(Transaction(oldTransactionJson))

		# Step 5: return populated items
		returnObj = {"items" : returnItems}
		if newTransactionId is not None:
			returnObj["transaction_id"] = newTransactionId 
		return returnObj