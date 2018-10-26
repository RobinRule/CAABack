from db.Transaction import Transaction
from global_var import Errors


import logging
logger = logging.getLogger(__name__)

class TransactionBusiness(object):
	"""docstring for TransactionBusiness"""
	
	@classmethod
	def consumeTransaction(cls, requesterId, transactionId, item):
		status, oldTransactionJson = Transaction.getItem(Transaction({'transactionId' : transactionId}))
		if not status:
			return { "error" : oldTransactionJson}
		
		# Step 1: verify that callerId is correct
		if oldTransactionJson['userId'] != requesterId:
			return { "error" : str(Errors.NotAuthoriedOperation)}

		# Step 2 : populate ids into items
		winSize = oldTransactionJson['winSize']
		itemIds = oldTransactionJson['itemIds']

		queryIds = itemIds if len(itemIds) <= winSize else itemIds[0:winSize]
		returnItems = item.getItemsByIds(queryIds, item)

		# Step 3: Generate a new trasaction
		newTransactionId = None
		if len(itemIds) > winSize:
			newTransactionJson = {
				'itemIds' : itemIds[winSize:],
				'winSize' : winSize,
				'timeToLive' : 10,
				'userId' : requesterId
			}
			newTransactionId = Transaction.addItem(Transaction(newTransactionJson))

		# Step 4: delete old transaction
		Transaction.deleteItem(Transaction(oldTransactionJson))

		# Step 5: return populated items
		returnObj = {"items" : returnItems}
		if newTransactionId is not None:
			returnObj["transaction_id"] = newTransactionId 
		return returnObj