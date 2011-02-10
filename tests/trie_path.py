import unittest
import sys
sys.path.append("../")
from Trieful import Trie, KEY_DOTTED, STORE_COUNT

def suite():
	suite = unittest.TestSuite()
	suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TriePathsTest))
	return suite
	
class TriePathsTest(unittest.TestCase):
	
	def setUp(self):
		self.trie = Trie(keyFunction = KEY_DOTTED, storeFunction = STORE_COUNT)
		self.keys = ['com.example', 'com.example.sub', 'org.example', 'com.other', 'com.other.sub', 'net.example', 'com.example.sub2']
		for key in self.keys:
			self.trie.add(key, 1)
	
	def test_has(self):
		for key in self.keys:
			self.assertTrue(self.trie.has(key), "Trie::has")
	
	def test_paths(self):
		
		comPaths = list(self.trie.paths(prefix = 'com'))
		examplePaths = list(self.trie.paths(prefix = 'com.example'))
		
		self.assertTrue(len(comPaths) == 5, "Trie::paths(prefix)")
		self.assertTrue(len(examplePaths) == 3, "Trie::paths(prefix)")