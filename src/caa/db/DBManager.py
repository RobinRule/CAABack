#!/usr/bin/python2.7
import sys
import sqlite3
import os
import logging
import decimal
from datetime import datetime
from .dynamodb.connectionManager import ConnectionManager
import json

logger = logging.getLogger(__name__)

sys.path.append(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        ".."
        )
    )
import global_var

use_instance_metadata = ""
if 'USE_EC2_INSTANCE_METADATA' in os.environ:
    use_instance_metadata = os.environ['USE_EC2_INSTANCE_METADATA']

# manages db connection
# singleton pattern, only one instance exist
class DBManager(object):
    """docstring for DBManager"""
    _CON = None

    @classmethod
    def dataToStr(cls, val):
        if type(val) is datetime:
            return "'{}'".format(val.isoformat())
        else:
            return val

    # return a connection
    @classmethod
    def connection(cls, mode = 'service'):
        if not cls._CON:
            cls._CON = ConnectionManager(
                mode=global_var.ARGS.mode,
                config=global_var.CFG,
                endpoint=global_var.ARGS.endpoint,
                port=global_var.ARGS.port,
                use_instance_metadata=use_instance_metadata
            )
        return cls._CON

    @classmethod
    def closeConnection(cls):
        logger.info("Closing database connection")
        cls._CON = None

    # return a table reference
    @classmethod
    def table(cls, table_name):
        return cls.connection().getTable(table_name)

    @classmethod
    def toJsonData(cls, item):
        # Helper class to convert a DynamoDB item to JSON.
        class DecimalEncoder(json.JSONEncoder):
            def default(self, o):
                if isinstance(o, decimal.Decimal):
                    return str(o)
                return super(DecimalEncoder, self).default(o)

        return json.loads(json.dumps(item, cls=DecimalEncoder))