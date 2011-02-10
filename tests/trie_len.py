import unittest
import sys
sys.path.append("../")
from Trieful import Trie, KEY_DOTTED, STORE_COUNT

def suite():
	suite = unittest.TestSuite()
	suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TrieLenTests))
	return suite
	
class TrieLenTests(unittest.TestCase):
	
	def setUp(self):
		self.trie = Trie(keyFunction = KEY_DOTTED, storeFunction = STORE_COUNT)
		self.keys = ['com.example', 'com.baz', 'com.example.sub', 'org.example', 'com.example', 'com.example.sub', 'com.example.sub']
		for key in self.keys:
			self.trie.add(key, 1)
	
	def test_has(self):
		for key in self.keys:
			self.assertTrue(self.trie.has(key), "Trie::has")
	
	def test_len(self):
		
		self.assertTrue(len(self.trie) == 4, "Trie::__len__")
	
	def test_removes(self):
		self.trie.remove('org.example')
		self.trie.remove('com.example')
		
		self.assertTrue(len(self.trie) == 3, "Trie::__len__")