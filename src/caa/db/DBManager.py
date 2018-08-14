#!/usr/bin/python2.7

import sys
import sqlite3
import os
import logging

logger = logging.getLogger(__name__)

sys.path.append(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        ".."
        )
    )
from app import CFG

# manages db connection
# singleton pattern, only one instance exist
class DBManager(object):
    """docstring for DBManager"""
    _CON = None
    
    # return a connection
    @classmethod
    def connection(cls):
        if not cls._CON:
            logger.info("Starting connection to database:{}".format(CFG["dblocation"]))
            cls._CON = sqlite3.connect(CFG["dblocation"])
        return cls._CON

    @classmethod
    def closeConnection(cls):
        logger.info("Closing database connection")
        cls._CON.close()
        cls._CON = None

    # return a cursor
    @classmethod
    def cursor(cls):
        return cls.connection().cursor()
