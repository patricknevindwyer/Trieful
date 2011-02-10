import unittest
import sys
sys.path.append("../")
from Trieful import Trie, KEY_DOTTED, STORE_COUNT

def suite():
	suite = unittest.TestSuite()
	suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TrieOpIadd))
	return suite
	
class TrieOpIadd(unittest.TestCase):
	
	def setUp(self):
		self.trie = Trie(keyFunction = KEY_DOTTED, storeFunction = STORE_COUNT)
		self.keys = ['com.example', 'com.example.sub', 'org.example']
		for key in self.keys:
			self.trie.add(key, 1)
	
	def test_has(self):
		for key in self.keys:
			self.assertTrue(self.trie.has(key), "Trie::has")
	
	def test_add_dict(self):
		
		addDict = {
			'com.example': 1,
			'com.example.sub2': 1,
			'org.other': 1,
			'org.example.sub': 1,
			'net.example': 1
		}
		
		self.trie += addDict
		
		self.assertTrue(len(self.trie) == 7, "Trie::__add__(dict) length")
		
		for key in addDict.keys():
			self.assertTrue(self.trie.has(key), "Trie::__add__(dict) contents")
		
		for key in self.keys:
			self.assertTrue(self.trie.has(key), "Trie::__add__(dict) contents")
	
	def test_add_mixedtrie(self):
		addTrie = Trie()
		
		self.assertRaises(TypeError, self.trie.__iadd__, addTrie)
		
	def test_add_trie(self):
		
		addDict = {
			'com.example': 1,
			'com.example.sub2': 1,
			'org.other': 1,
			'org.example.sub': 1,
			'net.example': 1
		}		
		addTrie = Trie(keyFunction = KEY_DOTTED, storeFunction = STORE_COUNT) + addDict
		
		self.trie += addTrie
		
		self.assertTrue(len(self.trie) == 7, "Trie::__add__(dict) length")
		
		for key in addDict.keys():
			self.assertTrue(self.trie.has(key), "Trie::__add__(dict) contents")
		
		for key in self.keys:
			self.assertTrue(self.trie.has(key), "Trie::__add__(dict) contents")
