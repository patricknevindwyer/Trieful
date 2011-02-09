import unittest
import sys
sys.path.append("../")
from Trieful import Trie, KEY_DOTTED

def suite():
	suite = unittest.TestSuite()
	suite.addTests(unittest.TestLoader().loadTestsFromTestCase(StringKeyTests))
	suite.addTests(unittest.TestLoader().loadTestsFromTestCase(DottedKeyTests))
	suite.addTests(unittest.TestLoader().loadTestsFromTestCase(KeyAsValueTests))
	return suite
	
class KeyAsValueTests(unittest.TestCase):

	def setUp(self):
		self.trie = Trie(keyFunction = KEY_DOTTED)
		self.keys = ['com.example', 'com.baz', 'com.example.sub', 'org.example']
		for key in self.keys:
			self.trie.add(key, key)
	
	def test_values(self):
		for k in self.keys:
			self.assertTrue(self.trie.get(k) == k, "Trie::get")
			
class DottedKeyTests(unittest.TestCase):
	
	def setUp(self):
		self.trie = Trie(keyFunction = KEY_DOTTED)
		self.keys = ['com.example', 'com.baz', 'com.example.sub', 'org.example']
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
	
	def test_allpathvalues(self):
		
		values = self.trie.getAllPathValues('com.example.sub')
		self.assertTrue(len(values) == 2, "Trie::getAllPathValues")
	
	def test_subpaths(self):
	
		subpaths = self.trie.getSubPaths('com.example.sub')
		self.assertTrue(len(subpaths) == 2, "Trie::getSubPaths")
		self.assertTrue(subpaths[0] == 'com.example', "Trie::getSubPaths")
		self.assertTrue(subpaths[1] == 'com.example.sub', "Trie::getSubPaths")
		
class StringKeyTests(unittest.TestCase):
	
	def setUp(self):
		self.trie = Trie()
		self.keys = ['bar', 'baz', 'barbell', 'foo', 'food', 'bar', 'bazbuzz', 'bazbuzz']
		
		for key in self.keys:
			self.trie.add(key, 1)
		
	def test_paths(self):
		paths = list(self.trie.paths())
		self.assertTrue(len(paths) == 6, "Trie::paths")
		
	def test_has(self):
		for key in self.keys:
			self.assertTrue(self.trie.has(key), "Trie::has")
			
	def test_in(self):
		for key in self.keys:
			self.assertTrue(key in self.trie, "Trie::__contains__")
	
	def test_get(self):
		for key in self.keys:
			self.assertTrue(self.trie.get(key) is not None, "Trie::get")
	
	def test_getItem(self):
		for key in self.keys:
			self.assertTrue(self.trie[key] is not None, "Trie::__getitem__")
			
	def test_remove(self):
		self.trie.remove('bar', 1)
		self.trie.remove('baz', 1)
		self.assertTrue(self.trie.get('bar') == 1, "Trie::remove")
		self.assertTrue(self.trie.get('baz') is None, "Trie::remove")

	
	def test_removeAll(self):
		self.trie.removeAll('bar')
		self.assertTrue(self.trie.get('bar') is None, "Trie::removeAll")
		self.assertTrue(self.trie.get('barbell') is not None, "Trie::removeAll retain leaves")
	
	def test_setItem(self):
		
		self.trie['blah'] = 1
		
		self.assertTrue(self.trie.get('blah') == 1, "Trie::__setitem__")
	
	def test_missingItems(self):
		notIn = ['bubbles', 'barb', 'bazz']
		
		for key in notIn:
			self.assertTrue(self.trie.get(key) is None, "Missing items")
		
	def test_singleItems(self):
		for item in ['baz', 'barbell', 'foo', 'food']:
			self.assertTrue(self.trie.get(item) == 1, "Trie::add non-duplicates")
	
	def test_doubleItems(self):
		for item in ['bar', 'bazbuzz']:
			self.assertTrue(self.trie.get(item) == [1, 1], "Trie::add duplicates")
	
	