import re
import nltk
from nltk.stem import PorterStemmer
import pymongo
from pymongo import Connection
from bson.objectid import ObjectId
import sys
sys.path.append("/home/I829287/fuzzy_adventure/db")
import mongo_api

def tokens(string):
	words = nltk.word_tokenize(string)
	tokenized = []
	for w in words:
		tokenized += w.split("_")
	
	un_cameled = []
	camel = re.compile("(.*)(Date|Name|Place)") # hard-coded for DBpedia
	for t in tokenized:
		out = camel.match(t)
		if out == None:
			un_cameled.append(t)
		else:
			un_cameled.append(out.group(1))
			un_cameled.append(out.group(2))

	stemmed = []
	for u in un_cameled:
		s = PorterStemmer().stem(u)
		stemmed.append(s.lower())

	filtered = filter(lambda s: s != '?' and s != ',' and s != '.' and s != "'s", stemmed)
	return filtered

def remove_stopwords(words):
	no_stopwords = [w.strip() for w in words if w.strip() not in nltk.corpus.stopwords.words('english')]
	return no_stopwords

def lexical_type(triplet):
	lex_type = 'unknown'
	title = triplet[title]
	types = {'name': ['name', 'surname', 'givenName'], 'date': ['birthDate', 'deathDate'], 'location': ['birthPlace', 'deathPlace'], 'occupation': ['description']}
	for type_name, titles in types.items():
		if title in titles:
			lex_type = type_name
	return lex_type

""" Accepts a triplet-dictionary instance and a list of search words.
It assumes that the user was looking for the information that is in the
triplet field that does NOT match anything in the search words. """
def extract_field(ids, words):
	output = []
	full_answers = []
	database = 'fuzzy_adventure'
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

""" Return a list of proper nouns, if a node is a proper noun """
def chunk(node):
	output = [node.word]
	if node.node_type == 'NNP' or node.node_type == 'NNPS':
		siblings = node.siblings()
		for s in siblings:
			if s.index == node.index+1:
				output.append(s.word)
	return output
