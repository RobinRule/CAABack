from mock import Mock, patch
import caa
from caa.db.Case import Case
import datetime
import sqlite3
import sys
import os
import unittest

from conftest import TST_DATA_PATH

testCase_record0 = [None, 0, 0, "New", datetime.datetime.now().isoformat(), None]
testCase_record1 = [None, 1, 1, "New", (datetime.datetime.now() + datetime.timedelta(days=1)).isoformat(), None]

DB_PATH = os.path.join(TST_DATA_PATH, "test.db")

# caa.app.CFG = { "dblocation" : DB_PATH }

class TestCase(unittest.TestCase):
	def setUp(self):
		conn = sqlite3.connect(DB_PATH)
		conn.execute('''
			CREATE TABLE CASES
       		(
       			caseId      INT       PRIMARY KEY NOT NULL,
       			usrId       INT       NOT NULL,
       			custId      INT       NOT NULL,
       			status      CHAR(15)  NOT NULL,
       			creatTime   TEXT      NULL,
       			closeTime   TEXT
       		);''')
		conn.commit()
		conn.close()

	def tearDown(self):
		os.remove(DB_PATH)

	@patch("caa.db.DBManager.CFG", { "dblocation" : DB_PATH })
	def test_CRUD(self):
		testCase0 = Case(testCase_record0)
		assert Case.addCase(testCase0) == 0
		testCase0.caseId = 0

		testCase1 = Case(testCase_record1)
		assert Case.addCase(testCase1) == 1
		testCase1.caseId = 1
		dbCase0 = Case.getCase(0)
		dbCase1 = Case.getCase(1)
		assert dbCase0 == testCase0, "{}!={}".format(dbCase0, testCase0)
		assert dbCase1 == testCase1, "{}!={}".format(dbCase1, testCase1)

		Case.delCase(0)
		assert Case.getCase(0) == None
		
		Case.updateCaseStatus(1, "In Progress")
		assert Case.getCase(1).status == "In Progress"
