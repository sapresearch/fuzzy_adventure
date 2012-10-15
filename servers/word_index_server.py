import sys
sys.path.append("../external/dbpediakit")
sys.path.append("../db")
import mongo_api
from SimpleXMLRPCServer import SimpleXMLRPCServer

def load_word_index():
	data = mongo_api.read_collection('person2')
	_, words = mongo_api.create_word_index(data, True)
	return words

def search(words):
	ids = []
	for synonyms in words:
		syn_ids = []
		for syn in synonyms:
			if syn in word_index:
				syns = word_index[syn]
				syn_ids += syns
		ids.append(set(syn_ids))
		
	intersection = ids[0]
	for i in ids[1:]:
		intersection = intersection & i
	intersection = list(intersection)
	intersection = [] if len(intersection) > 50 else intersection
	return intersection


word_index = load_word_index()

server = SimpleXMLRPCServer(('localhost', 9000), logRequests=True)
server.register_function(search)
server.serve_forever()
