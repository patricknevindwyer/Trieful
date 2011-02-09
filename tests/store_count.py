import unittest
import sys
sys.path.append("../")
from Trieful import Trie, KEY_DOTTED, STORE_COUNT

def suite():
	suite = unittest.TestSuite()
	suite.addTests(unittest.TestLoader().loadTestsFromTestCase(StoreCountTests))
	return suite
	
class StoreCountTests(unittest.TestCase):
	
	def setUp(self):
		self.trie = Trie(keyFunction = KEY_DOTTED, storeFunction = STORE_COUNT)
		self.keys = ['com.example', 'com.baz', 'com.example.sub', 'org.example', 'com.example', 'com.example.sub', 'com.example.sub']
		for key in self.keys:
			self.trie.add(key, 1)
	
	def test_has(self):
		for key in self.keys:
			self.assertTrue(self.trie.has(key), "Trie::has")
	
	def test_paths(self):
		for path in self.trie.paths():
			self.assertTrue(path in self.keys, "Trie::paths")
		
		paths = list(self.trie.paths())
		self.assertTrue(len(paths) == 4, "Trie::paths length")
	
	def test_counts(self):
		countParts = {
			'com.example': 2,
			'com.baz': 1,
			'com.example.sub': 3
		}
		
		for countPart in countParts.items():
			val = self.trie.get(countPart[0])
			self.assertTrue(val == countPart[1], "Trie::get with STORE_COUNT")
	
	def test_removes(self):
		self.trie.remove('org.example')
		self.trie.remove('com.example')
		
		self.assertTrue(self.trie.get('org.example') is None, "remove single path")
		self.assertTrue(self.trie.get('com.example') == 1, "remove double path")