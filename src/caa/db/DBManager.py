#!/usr/bin/python2.7

import sys
import sqlite3
import os
import logging
import boto3

logger = logging.getLogger(__name__)

sys.path.append(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        ".."
        )
    )
from global_var import CFG

# manages db connection
# singleton pattern, only one instance exist
class DBManager(object):
    """docstring for DBManager"""
    _CON = None
    
    # return a connection
    @classmethod
    def connection(cls):
        if not cls._CON:
            logger.info("Starting connection to database:{}".format(CFG["db"]))
            dbCfg = CFG["db"]
            cls._CON = boto3.resource(dbCfg["db"], region_name=dbCfg["region"], endpoint_url=dbCfg["endpoint"], aws_access_key_id="AKIAJWXA236SXOSTE2BA", aws_secret_access_key="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")
            # cls._CON = boto3.client('dynamodb', region_name='us-east-2', endpoint_url="http://dynamodb.us-east-2.amazonaws.com", aws_access_key_id="AKIAJWXA236SXOSTE2BA", aws_secret_access_key="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")
        return cls._CON

    @classmethod
    def closeConnection(cls):
        logger.info("Closing database connection")
        cls._CON = None

    # return a table reference
    @classmethod
    def table(cls, table_name):
        return cls.connection().Table(table_name)
