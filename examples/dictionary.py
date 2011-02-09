#!/usr/bin/python
import sys
sys.path.append("../")
from Trieful import Trie, STORE_COUNT
import time
from datetime import timedelta

if __name__ == "__main__":
	
	if len(sys.argv) == 1:
		print "Usage: %s <prefix 1> <prefix 2> . . . <prefix N>" % (sys.argv[0])
		print "\tFind how many words in the system dictionary have the given prefixes"
		sys.exit(1)
		
	prefixes = sys.argv[1:]
	print "Searching the following prefixes:"
	for p in prefixes:
		print "\t%s" % (p)
	
	t = Trie(storeFunction = STORE_COUNT)
	
	print "Building dictionary Trie"
	dictfile = open('/usr/share/dict/words', 'r')
	st = time.time()
	wordcount = 0
	for word in dictfile:
		wordcount += 1
		t.add(word.strip(), atAllSubPaths = True)
	ed = time.time()
	dictfile.close()
	
	print "\tBuilt Trie of %i words in %s" % (wordcount, str(timedelta(seconds = ed - st)))
	
	print "Number of words with prefixes:"
	st = time.time()
	for prefix in prefixes:
		print "\t%s:%i" % (prefix, t.get(prefix, defaultValue = 0))
	ed = time.time()
	print "Searching Trie for %i paths took %s" % (len(prefixes), str(timedelta(seconds = ed - st)))