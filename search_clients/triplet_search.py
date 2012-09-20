import xmlrpclib
import pymongo
from pymongo import Connection
from bson.objectid import ObjectId
import sys
sys.path.append("../")
sys.path.append("/home/I829287/fuzzy_adventure/models/")
sys.path.append("/home/I829287/fuzzy_adventure/")
sys.path.append("/home/I829287/fuzzy_adventure/external/dbpediakit")
import mongo_api
import synonym
import warnings

database = 'fuzzy_adventure'

def search(words):
	proxy = xmlrpclib.ServerProxy('http://localhost:9000')
	synonyms = []
	for word in words:
		syns = synonym.synonyms(word[0])
		synonyms.append(syns)
	results = proxy.search(synonyms)
	search_words = words[0] + words[1]
	selected_fields, full_answers = extract_field(results, search_words)
	return selected_fields, full_answers, synonyms

def extract_field(ids, words):
	output = []
	full_answers = []
	collection = Connection()[database]['person2']
	for i in ids:
		triplet = collection.find({'_id': ObjectId(i)})
		if triplet.count() > 0:
			sub = []
			sub += triplet # You have to do this to force the triplet from a cursor object to a dictionary. It's ridiculous, but it works.
			triplet = sub[0]
			full_answers.append([triplet['id'], triplet['text'], triplet['title']])
			field = mongo_api.select_field(triplet, words)
			output.append(field)
		else:
			warnings.warn("The word index returned an ID that wasn't found in the triplet collection")
	return output, full_answers
