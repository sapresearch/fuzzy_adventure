import sys
sys.path.append("../")
sys.path.append("../external/dbpediakit")
import mongo_api
from SimpleXMLRPCServer import SimpleXMLRPCServer
import time

server = SimpleXMLRPCServer(('localhost', 9000), logRequests=True)

def load_word_index():
	collection = 'word_index'
	print sys.getsizeof(collection)
	data = mongo_api.read_collection('person')
	_, words = mongo_api.create_word_index(data, True)
	return words

print 'Loading'
start = time.time()
word_index = load_word_index()

print sys.getsizeof(word_index)
print time.time() - start
print 'Ready'

def search(words):
	ids = []
	for synonyms in words:
		syn_ids = []
		for syn in synonyms:
			if syn in word_index:
				start = time.time()
				syns = word_index[syn]
				print "Time for " + syn + " " + str(time.time() - start)
				syn_ids += syns
		start = time.time()
		ids.append(list(set(syn_ids)))
		print "Append time " + str(time.time() - start)
	start = time.time()
	#intersection = mongo_api.intersection(ids)
	print len(ids[0])
	print len(ids[1])
	intersection = list(set(ids[0]) & set(ids[1]))
	print "intersection time " + str(time.time() - start)
	return intersection



server.register_function(search)
server.serve_forever()
