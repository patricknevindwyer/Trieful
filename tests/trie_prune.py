import unittest
import sys
sys.path.append("../")
from Trieful import Trie, KEY_DOTTED, STORE_COUNT

def suite():
	suite = unittest.TestSuite()
	suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TriePruneTests))
	return suite
	
class TriePruneTests(unittest.TestCase):
	
	def setUp(self):
		self.trie = Trie(keyFunction = KEY_DOTTED, storeFunction = STORE_COUNT)
		self.keys = ['com.example', 'com.example.sub', 'org.example', 'com.other', 'com.other.sub', 'net.example', 'com.example.sub2']
		for key in self.keys:
			self.trie.add(key, 1)
	
	def test_has(self):
		for key in self.keys:
			self.assertTrue(self.trie.has(key), "Trie::has")
	
	def test_paths(self):
		
		self.trie.prune('com.example.sub')
		comPaths = list(self.trie.paths(prefix = 'com'))
		self.assertTrue(len(comPaths) == 4, "Trie::paths(prefix)")
		
		self.trie.prune('com')
		comPaths = list(self.trie.paths(prefix = 'com'))
		self.assertTrue(len(comPaths) == 0, "Trie::paths(prefix)")
		
		self.assertTrue(len(self.trie) == 2, "Trie::__len__")