import xmlrpclib
import pymongo
from pymongo import Connection
from bson.objectid import ObjectId
import mongo_api
import sys
sys.path.append("../")
import time

database = 'fuzzy_adventure'

def search(words):
	proxy = xmlrpclib.ServerProxy('http://localhost:9000')
	x = [ ['america', 'germany', 'einstein'], ['birth', 'born', 'place'] ]
	start = time.time()
	results = proxy.search(words)
	#print time.time() - start
	#print len(results)
	#print results
	search_words = words[0] + words[1]
	return extract_field(results, search_words)

def extract_field(ids, words):
	output = []
	collection = Connection()[database]['person']
	for i in ids:
		triplet = collection.find({'_id': ObjectId(i)})
		sub = []
		sub += triplet # You have to do this to force the triplet from a cursor object to a dictionary. It's ridiculous, but it works.
		triplet = sub[0]
		field = mongo_api.select_field(triplet, words)
		output.append(field)
	return output
