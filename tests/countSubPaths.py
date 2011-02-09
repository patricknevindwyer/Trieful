import unittest
import sys
sys.path.append("../")
from Trieful import Trie, KEY_DOTTED, STORE_COUNT

def suite():
	suite = unittest.TestSuite()
	suite.addTests(unittest.TestLoader().loadTestsFromTestCase(SubPathCountTests))
	return suite
	
class SubPathCountTests(unittest.TestCase):
	
	def setUp(self):
		self.trie = Trie(keyFunction = KEY_DOTTED, storeFunction = STORE_COUNT)
		self.keys = ['com.example', 'com.blah', 'com.example.sub1', 'com.example.sub2']
		for key in self.keys:
			self.trie.add(key, 1, atAllSubPaths = True)
	
	def test_paths(self):
		for k in self.keys:
			self.assertTrue(k in self.trie, "Trie::paths has with atAllSubPaths")
			
	def test_counts(self):
		countParts = {
			'com': 4,
			'com.example': 3,
			'com.blah': 1,
			'com.example.sub1': 1,
			'com.example.sub2': 1
		}
		
		for countPart in countParts.items():
			val = self.trie.get(countPart[0])
			self.assertTrue(val == countPart[1], "Trie::get with atAllSubPaths")
	
	def test_removes(self):
		self.trie.remove('com.example.sub2', atAllSubPaths = True)
		countParts = {
			'com': 3,
			'com.example': 2,
			'com.blah': 1,
			'com.example.sub1': 1
		}		
		
		for countPart in countParts.items():
			val = self.trie.get(countPart[0])
			self.assertTrue(val == countPart[1], "Trie::remove with atAllSubPaths")