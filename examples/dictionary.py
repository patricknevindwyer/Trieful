#!/usr/bin/python
"""
Load a Trie with the contents of the shared Unix dictionary, and create a simple graph of which
two letter combinations start words. In the graph a '#' marks a combination that starts a known
word, while a blank denotes a prefix that does not exist.

This example uses:
	
	* The STORE_COUNT storage function
	* The Trie::add(atAllSubPaths) option to track all prefix combinations
	
"""
import sys
sys.path.append("../")
from Trieful import Trie, STORE_COUNT
import time
from datetime import timedelta

if __name__ == "__main__":

	# Setup a trie, using most of the defaults		
	t = Trie(storeFunction = STORE_COUNT)
	
	print "Building dictionary Trie"

	# Read all of the words from the shared dictionary, and add them to the Trie
	dictfile = open('/usr/share/dict/words', 'r')
	
	# track time and 
	st = time.time()
	wordcount = 0
	for word in dictfile:
		wordcount += 1
		t.add(word.strip(), atAllSubPaths = True)
	ed = time.time()
	dictfile.close()
	
	print "\tBuilt Trie of %i words in %s (%0.2f words / second)" % (wordcount, str(timedelta(seconds = ed - st)), (wordcount * 1.0) / (ed - st))
	
	print "Prefix graph"
	prefixes = "abcdefghijklmnopqrstuvwxyz"
	st = time.time()
	
	print "  %s" % (prefixes)
	print ""
	for rowPrefix in prefixes:
		rowData = [rowPrefix, " "]
		for colPrefix in prefixes:
			if t.get(rowPrefix + colPrefix, defaultValue = 0) > 0:
				rowData.append("#")
			else:
				rowData.append(" ")
		print "".join(rowData)
	
	ed = time.time()
	print "\nPrefix graph took %s" % (str(timedelta(seconds = ed - st)))
