#!/usr/bin/python
import types
import copy

KEY_DOTTED = {
	'pathToKey':lambda x: x.split('.'),
	'keyToPath':lambda x: '.'.join(x)
}

KEY_STRING = {
	'pathToKey': lambda x: x,
	'keyToPath': lambda x: x
}

"""
Default STORE FUNCTION

add: Append value to a list
remove: Remove first occurance of value from list
get: Return the list, or if the list is of length 1, return the only item in the list
"""
def store_default_add(old, new):
	if old is None:
		return [new]
	else:
		old.append(new)
		return old

def store_default_remove(obj, val):
	if val in obj:
		obj.remove(val)
		if len(obj) == 0:
			return None
		else:
			return obj
	else:
		return obj
	
def store_default_get(obj):
	if len(obj) == 1:
		return obj[0]
	else:
		return obj

STORE_DEFAULT = {
	'add': store_default_add,
	'remove': store_default_remove,
	'get': store_default_get
}

"""
Overwrite STORE FUNCTION

Enforce one value per path. This is, in effect, a standard Trie mapping.

add: Replace node value with new value
remove: Remove node
get: Retrieve node value
"""
def store_ow_add(old, new):
	return new

def store_ow_remove(obj, val):
	return None

def store_ow_get(obj):
	return obj
	
STORE_OVERWRITE = {
	'add': store_ow_add,
	'remove': store_ow_remove,
	'get': store_ow_get
}

"""
Addition STORE FUNCTION

This storage function is based on adding values, regardless of type.

add: add (append) value to existing value
remove: subtract value from existing value
get: retrieve raw value
"""
def store_add_add(old, new):
	if old is None:
		return new
	else:
		return old + new

def store_add_remove(old, new):
	return old - new

def store_add_get(old):
	return old
	
STORE_ADD = {
	'add': store_add_add,
	'remove': store_add_remove,
	'get': store_add_get
}

"""
Count STORE FUNCTION

Count occurances via increment.

add: increment by one
remove: decrement by one (None at zero)
get: retrieve value
"""
def store_count_add(old, new):
	if old is None:
		return 1
	else:
		return old + 1
		
def store_count_remove(old, new):
	ret = old - 1
	if ret == 0:
		return None
	else:
		return ret

def store_count_get(obj):
	return obj
	
STORE_COUNT = {
	'add': store_count_add,
	'remove': store_count_remove,
	'get': store_count_get
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
			
	- key functions and storage functions for suffix tries
		http://en.wikipedia.org/wiki/Suffix_tree
		
	- example for interleaved levenstein trie
	
	- allow for packing/compressing trie by turning off add/remove when trie is filled
		- set a read/write mode
		- array packing or prefix compression
	
	- longest prefix matching
		http://en.wikipedia.org/wiki/Longest_prefix_match
	
	- case insensitive / sensitive comparisons
	
	- fast prefix counting
	
	- fast loading
		
	- paths from node:
		
		find all base paths:
			t.subPathsOf("")
		
		find all stemmed:
			t.subPathsOf("dis")
			
	- speed tests
	
	- examples
	
	- __sub__ method
		Remove subsets of a Trie to a new structure (by prefix)
		
		needs items() and startswith()
		
		find prefixes to remove with startswith
		iterate all items with items() to create new structure
		
		!!or deep copy internal structure and removeall/prune
		
	- -= method
	
	= AND (&) OR (|) XOR(^) operations
		
		set operations
						
	- __mod__ method
	
		trie:
			find any paths _not_ in other trie
		
		other:
			find any paths _not_ in prefix generated from _other_
			
		Find subset containing only prefix
		
		find prefix, deep copy, hand build prefix structure
			
	- comparisons
	
	- base iterator/generator (items generator)
	- follow dict base
		- items
		- iteritems
		- iterkeys
		- itervalues
	- (keys|values|items)_startswith() method
		
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

	
	def __init__(self, keyFunction = None, defaultValue = None, storeFunction = None):

		self._nodes = {}
		self._size = 0
		
		if storeFunction is None:
			self._storeFunction = STORE_DEFAULT
		else:
			self._storeFunction = storeFunction
			
		if keyFunction is None:
			self._keyFunction = KEY_STRING
		else:
			self._keyFunction = keyFunction
		
		self._defaultValue = defaultValue
		
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
		
	def add(self, path, value = None, atAllSubPaths = False):
		"""
		Map the path key to the given object.
		"""
		addObj = value
		if addObj is None:
			addObj = self._defaultValue
			
		baseNode = self._nodes
		lastNodeAdded = False
		
		for comp in self._pathToKey(path):
			if comp not in baseNode:
				baseNode[comp] = {}
			baseNode = baseNode[comp]
			
			# add to this subpath
			if atAllSubPaths:
				if '__' not in baseNode:
					lastNodeAdded = True
					baseNode['__'] = self._storeFunction['add'](None, addObj)
				else:
					lastNodeAdded = False
					oldValue = baseNode['__']
					baseNode['__'] = self._storeFunction['add'](oldValue, addObj)

		if not atAllSubPaths:
			if '__' not in baseNode:
				lastNodeAdded = True
				baseNode['__'] = self._storeFunction['add'](None, addObj)
			else:
				lastNodeAdded = False
				oldValue = baseNode['__']
				baseNode['__'] = self._storeFunction['add'](oldValue, addObj)
		
		if lastNodeAdded:
			self._size += 1
			
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
		self._size -= 1
		
		# if the node is now empty, delete it
		if len(baseNode[leafPath].keys()) == 0:
			del baseNode[leafPath]
		
	def __delitem__(self, path):
		self.removeAll(path)
		
	def remove(self, path, value = None, atAllSubPaths = False):
		"""
		Remove a specific item of the path, and leave any others in place.
		"""
		
		remObj = value
		if remObj is None:
			remObj = self._defaultValue
			
		baseNode = self._nodes
		pathKey = self._pathToKey(path)
		
		for comp in pathKey[:-1]:
			if comp not in baseNode:
				return
			baseNode = baseNode[comp]
			
			if atAllSubPaths:
				if '__' in baseNode:
					baseNode['__'] = self._storeFunction['remove'](baseNode['__'], remObj)
				
					if baseNode['__'] is None:
						del baseNode['__']
			
		
		# see if the tail leaf exists
		leafPath = pathKey[-1]
		if leafPath not in baseNode:
			return
			
		# remove any values
		baseNode[leafPath]['__'] = self._storeFunction['remove'](baseNode[leafPath]['__'], remObj)
		
		if baseNode[leafPath]['__'] is None:
			del baseNode[leafPath]['__']
			self._size -= 1
			
		# if the node is now empty, delete it
		if len(baseNode[leafPath].keys()) == 0:
			del baseNode[leafPath]
	
	def __len__(self):
		return self._size
		
	def prune(self, path):
		"""
		Remove an entire branch of the path, including child nodes and paths.
		"""
		
		prunePaths = list(self.paths(prefix = path))
		
		for prunePath in prunePaths:
			self.removeAll(prunePath)
		# make sure structure is pruned completely
		
		
	def get(self, path, defaultValue = None):
		"""
		Retrieve the objects mapped to this path key.
		"""
		baseNode = self._nodes
		
		for comp in self._pathToKey(path):
			if comp not in baseNode:
				return defaultValue
			baseNode = baseNode[comp]
		
		if '__' not in baseNode:
			return defaultValue
		else:
			ret = self._storeFunction['get'](baseNode['__'])
			if ret is not None:
				return ret
			else:
				return defaultvalue
	
	def __getitem__(self, path):
		return self.get(path)
	
	def __iadd__(self, other):
		"""
		Handle in place addition of objects to the Trie. Suppoted right
		hand operands:
			
			- Trie
			- Dictionary
		
		In the case of adding Tries, the keyFunction and storeFunction must
		agree, or a TypeError will be raised.
		"""
		
		if type(other) == types.DictType:

			for (k, v) in other.items():
				self.add(k, v)
				
			return self
			
		elif isinstance(other, Trie):

			if self._keyFunction != other._keyFunction:
				raise TypeError("Trie keyFunctions don't match")
			elif self._storeFunction != other._storeFunction:
				raise TypeError("Trie storeFunctions don't match")
			
			for (k, v) in other.items():
				self.add(k, v)
			
			return self
		else:
			raise TypeError("Unsupported type added to trie: %s" % (type(other)))
		
	def __add__(self, other):
		"""
		Add the contents of the right hand operand to a new trie. The current
		Trie is deep copied into a new Trie, and the contents of the right
		hand operand iterated to add to the new Trie.
		
		Supported right hand operands:
		
			- Trie
			- Dictionary
			
		In the case of adding Tries, the keyFunction and storeFunction must
		agree, or a TypeError will be raised.
		"""
		
		if type(other) == types.DictType:
		
			# duplicate the current Trie
			nt = self._deepcopy()
			
			for (k, v) in other.items():
				nt.add(k, v)
			
			return nt
			
		elif isinstance(other, Trie):
		
			if self._keyFunction != other._keyFunction:
				raise TypeError("Trie keyFunctions don't match")
			elif self._storeFunction != other._storeFunction:
				raise TypeError("Trie storeFunctions don't match")
				
			# duplicate self
			nt = self._deepcopy()
			
			# merge the other trie data
			for (k, v) in other.items():
				nt.add(k, v)
			
			return nt
		else:
			raise TypeError("Unsupported type added to Trie: %s" % (type(other)))
	
	def __mod__(self, other):
		"""
		"""
		pass
		
	def _deepcopy(self):
		nt = Trie(storeFunction = self._storeFunction, keyFunction = self._keyFunction)
		nt._nodes = copy.deepcopy(self._nodes)
		nt._size = self._size
		return nt
		
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
	
	def items(self):
		
		for path in self.paths():
			yield (path, self[path])
			
	def paths(self, prefix = None):
		"""
		Return all of the paths stored in the Trie.
		"""
		
		stack = []
		pathPrefix = None
		if prefix is not None:
			pathPrefix = self._pathToKey(prefix)
			
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
				if pathPrefix is None:
					yield self._keyToPath(pathTuple[0])
				else:
					if pathPrefix == pathTuple[0][:len(pathPrefix)]:
						yield self._keyToPath(pathTuple[0])
	
	def __repr__(self):
		
		return str(self._nodes)