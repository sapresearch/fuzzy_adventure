import pymongo
from pymongo import Connection
import sys
sys.path.append('./external/dbpediakit')
import dbpediakit as dbk
import dbpediakit.archive
import time
import nltk as nltk
import copy

database = 'fuzzy_adventure'

""" Accepts a list of lists. Each list is inserted in bulk into Mongo.
If the list is too large, then Mongo crashes. We're been using lists of 100,000 elements."""
def write_collection(data, collection):
	connection = Connection()
	db = connection[database]
	c = db[collection]
	for d in data:
		c.insert(d)
	return None

def read_collection(collection):
	connection = Connection()
	db = connection[database]
	output = db[collection].find()
	return output

""" Loads DBpedia information so that it can be saved into a MongoDB collection.
When you use the DBpediaKit to pull data from DBpedia, it downloads it with a TCP connection
and then saves it in a local cached in ~/data/dbpedia/filename. This function accesses that
cache.  Each record is put into a list with no more than 100,000 elements.  Each list of 100,000
elements is put into a master list, and this master list is returned.
Example: output = [ [{record1} .... {record100,000}], [{record100,001} ... {record200,000}] ]"""
def load_dbpedia():
	archive_file = dbk.archive.fetch("persondata")
	tuples = dbk.archive.extract_triple(archive_file)

	output = []
	sub_out = []
	limit = 100000
	count = 0
	for record in tuples:
		count += 1
		r = {"id": record.id, "title":record.title, "text":record.text}
		sub_out.append(r)
		if count == limit:
			print count
			count = 0
			copied = copy.copy(sub_out)
			output.append(copied)
			sub_out = []
	return output

""" Accepts a list of DBpedia records that we have saved in another Mongo collection.
It returns a list that is suitable to be used to create another Mongo collection.
This is a list of hashes: [ {'word':'hello', 'ids':'the ids where that word was used'} ]
After this list has been saved as a new Mongo collection, it can then be queried to
find all the IDs in the other collection where that word occured."""
def create_word_index(data):
	words = {}
	for record in data:
		text = ' '.join([record['id'], record['title'], record['text']])
		text = text.replace('.', '')
		tokens = nltk.word_tokenize(text)
		tokens = filter(lambda a: a != '.', tokens)
		mongo_id = record['_id']
		for word in tokens:
			if word in words:
				words[word].append(mongo_id)
			elif word not in words:
				words[word] = [mongo_id]

	output = []
	sub_out = []
	limit = 100000
	count = 0
	for word,ids in words.items():
		count += 1
		sub_out.append({'word':word, 'ids':ids})
		if count == limit:
			print count
			count = 0
			copied = copy.copy(sub_out)
			output.append(copied)
			sub_out = []
	return output

""" Search for a single word."""
def word_search(word):
	connection = Connection()
	result = connection[database]['word_index'].find({'word':word})
	return result

""" Return the IDs for the relational triples. """
def ids_for_word(word):
	ids = []
	for w in word_search(word):
		ids += w['ids']
	return ids
	
""" Find the intersection for two words (ie the IDs of 
the relational triples that have both of the words."""
def intersection(word1, word2):
	word1 = ids_for_word(word1)
	word2 = ids_for_word(word2)
	intersect = list(set(word1) & set(word2))
	return intersect

def union(a,b):
	return list(set(a) | set(b))
