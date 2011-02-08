#!/usr/bin/python

import unittest
import tests.keys
#from tests.keys import StringKeyTests, suite as suite_keys
from Trieful import Trie

if __name__ == "__main__":
		
	suite = unittest.TestSuite()
	suite.addTests(tests.keys.suite())
	unittest.TextTestRunner(verbosity=2).run(suite)