#!/usr/bin/python

KEY_DOTTED = {
	'pathToKey':lambda x: x.split('.'),
	'keyToPath':lambda x: '.'.join(x)
}

KEY_STRING = {
	'pathToKey': lambda x: x,
	'keyToPath': lambda x: x
}

class Trie(object):
	"""
	A fast, non-recursive Trie structure. Keys can be any iterable data type, and
	stored objects can be any data structure. Keys map to multiple values.
	
	An optinal _keyFunction_ for the Trie makes it easy to convert keys into the
	desired mapping keys (see example below).
	
	Algorithmic Efficiency
	======================
	add: O(n) on the path key (worst case)
	get: O(n) on the path key (worst case)
	has
	remove
	removeAll
	prune!!
	value storage mode
		- append vs dict vs function (object manager) vs _count_ vs _countall_ (rainbird-esque)
		
	Examples
	========
	Check word spelling with a fast access data structure:
		
		# find words in a document that aren't in the shared dictionary
		t = Trie()
		
		wordfile = open('/usr/share/dict/words', 'r)
		for word in wordfile:
			word.strip()
			t.add(word, 1)
		wordfile.close()
		
		document = open(pathToDocument, 'r').read()
		for word in document.split():
			if not t.has(word):
				print word

	The Trie can be configured with a _keyFunction_ to be applied to every
	incoming key to turn it into an iterable sequence:
		
		def dottedKey(v):
			return v.split('.')
		
		t = Trie(keyFunction = dottedKey)
		
		# Key is ['ui', 'summary', 'file']
		t.add('ui.summary.file', funcA)
		
		# get the function
		myFunc = t['ui.summary.file']
		
	Upcoming Features
	=================
		
	- speed tests
	
	- examples
	
	- __sub__ method
		Remove subsets of a Trie to a new structure (by prefix)
		
		needs items() and startswith()
		
		find prefixes to remove with startswith
		iterate all items with items() to create new structure
		
		!!or deep copy internal structure and removeall/prune
		
	- -= method
	
	- __add__ method
		Merge Trie with other Tries or data structures
		
		deep copy one, merge data from other using dict::update
		keyFunction must agree
		
	- += method
		
		direct merge into primary
		
	- __mod__ method
		Find subset containing only prefix
		
		find prefix, deep copy, hand build prefix structure
		
	- __len__ method
		
		- track number of keys at top level
		
	- comparisons
	
	- base iterator/generator (items generator)
	
	- (keys|values|items)_startswith() method
	
	- storage function | mode
		- by function (custom)
			- SET
			- APPEND
			- COUNT
			- OVERWRITE
		- mode (count | append | overwrite)
	
	- value sorting/searching
	
	- Trie walk
	
	- method chaining
	
	- functional methods (apply all | map | etc)
	
	- serialization
	
	- __repr__
	
	- prune() method
		
	- prefix search
	
	- find by regex
	
	"""

	
	def __init__(self, keyFunction = None):
		self._nodes = {}
		if keyFunction is None:
			self._keyFunction = KEY_STRING
		else:
			self._keyFunction = keyFunction

	def _pathToKey(self, p):
		"""
		Generate a key path based on the optionally configured keyFunction.
		"""
		return self._keyFunction['pathToKey'](p)

	def _keyToPath(self, k):
		"""
		Given a key, reconstitute the original path
		"""
		return self._keyFunction['keyToPath'](k)
		
	def add(self, path, obj):
		"""
		Map the path key to the given object.
		"""
		baseNode = self._nodes
		
		for comp in self._pathToKey(path):
			if comp not in baseNode:
				baseNode[comp] = {}
			baseNode = baseNode[comp]
				
		if '__' not in baseNode:
			baseNode['__'] = [obj]
		else:
			baseNode['__'].append(obj)
	
	def __setitem__(self, path, obj):
		"""
		Set an item using the square bracket accessors
		"""
		self.add(path, obj)
		
	def removeAll(self, path):
		"""
		Remove all of the items associated with this path. This does not delete sub paths, only
		the current objects of the path.
		"""
		
		baseNode = self._nodes
		pathKey = self._pathToKey(path)
		
		for comp in pathKey[:-1]:
			if comp not in baseNode:
				return
			baseNode = baseNode[comp]
		
		# see if the tail leaf exists
		leafPath = pathKey[-1]
		if leafPath not in baseNode:
			return
			
		# remove any values
		del baseNode[leafPath]['__']
		
		# if the node is now empty, delete it
		if len(baseNode[leafPath].keys()) == 0:
			del baseNode[leafPath]
		
	def __delitem__(self, path):
		self.removeAll(path)
		
	def remove(self, path, obj):
		"""
		Remove a specific item of the path, and leave any others in place.
		"""
		
		baseNode = self._nodes
		pathKey = self._pathToKey(path)
		
		for comp in pathKey[:-1]:
			if comp not in baseNode:
				return
			baseNode = baseNode[comp]
		
		# see if the tail leaf exists
		leafPath = pathKey[-1]
		if leafPath not in baseNode:
			return
			
		# remove any values
		if obj in baseNode[leafPath]['__']:
			baseNode[leafPath]['__'].remove(obj)
		
		if len(baseNode[leafPath]['__']) == 0:
			del baseNode[leafPath]['__']
			
		# if the node is now empty, delete it
		if len(baseNode[leafPath].keys()) == 0:
			del baseNode[leafPath]
		
	def prune(self, path):
		"""
		Remove an entire branch of the path, including child nodes and paths.
		"""
		pass
		
	def get(self, path):
		"""
		Retrieve the objects mapped to this path key.
		"""
		baseNode = self._nodes
		
		for comp in self._pathToKey(path):
			if comp not in baseNode:
				return None
			baseNode = baseNode[comp]
		
		if '__' not in baseNode:
			return None
		else:
			ret = baseNode['__']
			if len(ret) == 1:
				return ret[0]
			else:
				return ret
	
	def __getitem__(self, path):
		return self.get(path)
		
	def getSubPaths(self, path):
		"""
		Retrieve the given path (if it is a valid path), as well as
		any valid sub paths:
			t = Trie()
			t.add("asd", 1)
			t.add("asdf", 1)
			t.add("adf", 1)
			
			paths = t.getSubPaths('asdf')
			
			paths == ['asd', 'asdf']
		"""
		key = self._pathToKey(path)
		
		keyBits = []
		keyPaths = []
		
		baseNode = self._nodes
		
		for k in key:
			keyBits.append(k)
		
			if k not in baseNode:
				break
			
			baseNode = baseNode[k]
			
			if '__' in baseNode:
				keyPaths.append(self._keyToPath(keyBits))

		
		return keyPaths
		
	def getAllPathValues(self, path):
		"""
		Retrieve the values mapped to the path key, including
		any path along the way that contains leaf values. This is
		especially useful when constructing domain based listeners:
			
			# add some listeners
			listeners = Trie()
			listeners.add("ui.summary".split("."), functionA)
			listeners.add("ui.summary.file".split("."), functionB)
			
			# retrieve a specific listener
			#	[functionB]
			funcs = listeners.get("ui.summary.file".split("."))
			
			# retrieve the path of listeners
			#	[functionA, functionB]
			funcs = listeners.getAllPathLeaves("ui.summary.file".split("."))
		
		Returned mapped values are in heirarchical order
		"""
		retValues = []
		
		baseNode = self._nodes
		
		for comp in self._pathToKey(path):
			if comp not in baseNode:
				return None
			if '__' in baseNode:
				retValues += baseNode['__']
			baseNode = baseNode[comp]
		
		if '__' not in baseNode:
			return None
		else:
			return retValues + baseNode['__']
		
	def has(self, path):
		"""
		Return true if a path exists, otherwise false.
		"""
		baseNode = self._nodes
		for comp in self._pathToKey(path):
			if comp not in baseNode:
				return False
			baseNode = baseNode[comp]
		
		return True if '__' in baseNode else False
	
	def __contains__(self, path):
		"""
		The _in_ or __contains__ operator maps to the _has_ method. So the two examples
		below are identical:
			
			trie.has('mypath')
			'mypath' in trie
		"""
		return self.has(path)
		
	def paths(self):
		"""
		Return all of the paths stored in the Trie.
		"""
		
		stack = []
		
		# prime the stack with the base prefixes
		baseNode = self._nodes
		startKeys = baseNode.keys()
		startKeys.sort()
		startKeys.reverse()
		
		for key in startKeys:
			stack.append( ([key], baseNode[key]) )
		
		# loop through the stack until complete
		while len(stack) > 0:
			
			# get the last item on the stack, and add
			# any keys to the stack
			pathTuple = stack.pop()
			
			pathKeys = pathTuple[1].keys()
			if '__' in pathKeys:
				pathKeys.remove('__')
			pathKeys.sort()
			pathKeys.reverse()
			for pathKey in pathKeys:
				stack.append( (pathTuple[0] + [pathKey], pathTuple[1][pathKey]) )
				
			# if their is a leaf, yield this path
			if '__' in pathTuple[1]:
				yield self._keyToPath(pathTuple[0])
	
	def __repr__(self):
		
		return str(self._nodes)