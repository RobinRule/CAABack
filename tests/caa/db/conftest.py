
import sys
import os

PRJ_PATH = os.path.abspath(
	os.path.join(
		os.path.dirname(os.path.abspath(__file__)),
		"../../.."
		)
	)
SRC_PATH = os.path.join(PRJ_PATH, "src")
TST_PATH = os.path.join(PRJ_PATH, "tests")
TST_DATA_PATH = os.path.join(TST_PATH, "data")

sys.path.append(SRC_PATH)