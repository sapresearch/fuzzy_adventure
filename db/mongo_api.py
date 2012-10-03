import pymongo
from pymongo import Connection
from bson.objectid import ObjectId
import sys
sys.path.append("/home/I829287/fuzzy_adventure/external/dbpediakit")
sys.path.append("/home/I829287/fuzzy_adventure/query_decomposition")
import dbpediakit as dbk
import dbpediakit.archive
import nlp
import copy

database = 'fuzzy_adventure'

""" Accepts a list of lists. Each list is inserted in bulk into Mongo.
If the list is too large, then Mongo crashes. We're been using lists of 100,000 elements."""
def write_collection(data, collection):
	connection = Connection()
	db = connection[database]
	c = db[collection]
	for d in data:
		print "Memory: " + str(sys.getsizeof(d))
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
			print r
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
def create_word_index(data, string=False):
	words = {}
	#count = 0
	for record in data:
		#count += 1
		#if count >= 50000:
			#print words
			#return words
		text = ' '.join([record['id'], record['title'], record['text']])
		text = text.replace('.', '')
		tokens = nlp.tokens(text)
		mongo_id = record['_id']
		if string == True:
			mongo_id = str(mongo_id.__str__())
		for word in tokens:
			if word in words:
				words[word].append(mongo_id)
			elif word not in words:
				words[word] = [mongo_id]

	output = []
	sub_out = []
	limit = 20000
	count = 0
	for word,ids in words.items():
		count += 1
		sub_out.append({'word':word, 'ids':ids})
		if count == limit:
			count = 0
			copied = copy.copy(sub_out)
			output.append(copied)
			sub_out = []
	return output, words

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
def intersection(words):
	if len(words) == 0:
		return []
	all_ids = set(ids_for_word(words[0]))
	for w in words:
		ids = ids_for_word(w)
		all_ids = all_ids & set(ids)
	return list(all_ids)

def union(words):
	all_ids = set([])
	for w in words:
		all_ids = all_ids | set(w)
	return list(all_ids)

def find_by_words(words):
	ids = intersection(words)
	output = []
	collection = Connection()[database]['person2']
	for i in ids:
		triplet = collection.find({'_id': ObjectId(i)})
		sub = []
		sub += triplet # You have to do this to force the triplet from a cursor object to a dictionary. It's ridiculous, but it works.
		triplet = sub[0]
		output.append(select_field(triplet, words))
	return output

""" Find the missing field from the triplet. Assume that
if a word occurs in two out of three fields, then the third
field is the one that the person was looking for.  If it isn't
found, then guess. """
def select_field(triplet, search_words):
	fields = ['text', 'id', 'title']
	missing = copy.copy(fields)
	for f in fields:
		field_tokens = nlp.tokens(triplet[f])
		for search in search_words:
			if search in field_tokens:
				missing = filter(lambda m: m != f, missing)
	missing_field = fields[0] if len(missing) == 0 else missing[0]
	output = triplet[missing_field]
	return output
