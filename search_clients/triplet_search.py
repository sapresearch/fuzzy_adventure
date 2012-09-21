import xmlrpclib
import pymongo
from pymongo import Connection
from bson.objectid import ObjectId
import sys
sys.path.append("/home/I829287/fuzzy_adventure")
sys.path.append("/home/I829287/fuzzy_adventure/models")
sys.path.append("/home/I829287/fuzzy_adventure/db")
sys.path.append("/home/I829287/fuzzy_adventure/external/dbpediakit")
import mongo_api
import synonym
import warnings
import nlp

def search(words):
	synonyms = format_triplet(words)
	proxy = xmlrpclib.ServerProxy('http://localhost:9000')
	results = proxy.search(synonyms)
	search_words = [item for sublist in synonyms for item in sublist] # flatten it
	selected_fields, full_answers = nlp.extract_field(results, search_words)
	return selected_fields, full_answers, synonyms

def format_triplet(words):
	chunked = []
	for w in words:
		chunked += nlp.chunk(w)
	
	# put it into an array of subarrays, with each word and it's synonyms in a subarray
	triplet = []
	for c in chunked:
		syns = synonym.synonyms(c)
		string = " ".join(syns)
		tokens_list = nlp.tokens(string)
		triplet.append(tokens_list)
	
	return triplet
