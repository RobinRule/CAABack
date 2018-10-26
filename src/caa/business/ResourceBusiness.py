from db.Resource import Resource
from global_var import CFG

import boto3

import logging
logger = logging.getLogger(__name__)

params = {}
params['aws_access_key_id'] = CFG.get('aws_credential', 'aws_access_key_id')
params['aws_secret_access_key'] = CFG.get('aws_credential', 'aws_secret_access_key')
BUCKET = CFG.get("s3", "bucket")
S3_CLIENT = boto3.client("s3", **params)
class ResourceBusiness(object):
	"""docstring for ResourceBusiness"""
	
	# upload resource to S3 bucket, delete the file when it's done
	@classmethod
	def uploadResource(cls, requesterId, resourceId, filePath):
		# Step 1: verify that it's the right requester that upload this file

		# Step 2: upload file
		try:
			S3_CLIENT.upload_file(filePath, BUCKET, resourceId)
		except Exception as e:
			logger.exception("Failed to upload file:{} to s2".format(resourceId))
			return {"error" : "Unknown error happended when uploading file."}

		# Step 3: delete file
		os.remove(filePath)

		return { "status" : True}