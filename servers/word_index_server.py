import sys
sys.path.append("../")
sys.path.append("../external/dbpediakit")
sys.path.append("../db")
import mongo_api
from SimpleXMLRPCServer import SimpleXMLRPCServer
import time

server = SimpleXMLRPCServer(('localhost', 9000), logRequests=True)

def load_word_index():
	collection = 'word_index'
	print sys.getsizeof(collection)
	data = mongo_api.read_collection('person2')
	_, words = mongo_api.create_word_index(data, True)
	return words

print 'Loading'
start = time.time()
word_index = load_word_index()
print "Ready. Load time for word index: " + str(time.time() - start)

def search(words):
	ids = []
	for synonyms in words:
		syn_ids = []
		for syn in synonyms:
			if syn in word_index:
				syns = word_index[syn]
				syn_ids += syns
		ids.append(list(set(syn_ids)))
	#intersection = mongo_api.intersection(ids)
	print len(ids[0])
	print len(ids[1])
	start = time.time()
	# This is ugly coding, but finding the intersection of the sets iteratively takes much longer.
	# TODO Right now it's hardcoded for 2 or 3 synonym sets.  This needs to be more general.
	if len(ids) == 2:
		intersection = list(set(ids[0]) & set(ids[1]))
	elif len(ids) == 3:
		print len(ids[2])
		intersection = list(set(ids[0]) & set(ids[1]) & set(ids[2]))
	print "intersection time " + str(time.time() - start) + "\n"
	return intersection



server.register_function(search)
server.serve_forever()
