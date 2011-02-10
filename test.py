#!/usr/bin/python

import unittest
import tests.keys
import tests.store_count
import tests.countSubPaths
import tests.trie_len
import tests.trie_items
import tests.trie_add

from Trieful import Trie

if __name__ == "__main__":
		
	suite = unittest.TestSuite()
	suite.addTests(tests.keys.suite())
	suite.addTests(tests.store_count.suite())
	suite.addTests(tests.countSubPaths.suite())
	suite.addTests(tests.trie_len.suite())
	suite.addTests(tests.trie_items.suite())
	suite.addTests(tests.trie_add.suite())
	unittest.TextTestRunner(verbosity=2).run(suite)