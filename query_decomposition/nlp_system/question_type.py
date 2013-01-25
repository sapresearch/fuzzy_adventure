from sklearn import tree
from sklearn.ensemble import ExtraTreesClassifier
from numpy import *
import sys
#sys.path.append("/home/I829287/fuzzy_adventure/test")
import word_space
sys.path.append("../")
#import load_data
import re

vector_length = 100

def train(questions, types):
	question_arrays = []
	for q in questions:
		question_arrays.append(q.split(" "))

	word_vector_hash = word_space.word_vectors(question_arrays)
	questions = question_vectors(word_vector_hash, question_arrays)

	xtrees = ExtraTreesClassifier(n_estimators=10, max_depth=None, min_samples_split=1, random_state=0)
	model = xtrees.fit(questions, types)
	return model, word_vector_hash

def question_vectors(word_vector_hash, questions):
	question_vectors = []
	for q in questions:
		vect = zeros(vector_length)
		for word in q:
			if word in word_vector_hash:
				vect += word_vector_hash[word]
		question_vectors.append(vect)
	return question_vectors

def classify(query, model=None, word_vector_hash=None):
	pred = hardcode(query)
	if pred != None:
		return pred
	if model == None or word_vector_hash == None:
		file_path = "/home/I829287/fuzzy_adventure/test/test_data.txt"
		questions, _, types = load_data.load_data(file_path)
		model, word_vector_hash = train(questions, types)
	q = query.split(" ")
	q_vect = question_vectors(word_vector_hash, [q])[0]
	pred = model.predict(q_vect)[0]
	return pred

def hardcode(query):
	lat = None
	when = re.search("^(When|What (date|year|day|month)).*", query)
	if type(when) != type(None):
		lat = 'date'
	where = re.search("^(Where|What (town|city|region|country)).*", query)
	if type(where) != type(None):
		lat = 'location'
	return lat
