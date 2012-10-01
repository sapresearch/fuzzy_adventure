from sklearn import tree
from sklearn.ensemble import ExtraTreesClassifier
from numpy import *
import sys
sys.path.append("/home/I829287/fuzzy_adventure/test")
sys.path.append("/home/I829287/fuzzy_adventure")
import fuzzy_adventure
import word_space
import time

vector_length = 100

def train(file_path):
	questions, _, types = fuzzy_adventure.load_data(file_path)
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

def classify(question):
	s = time.time()
	model, word_vector_hash = train("/home/I829287/fuzzy_adventure/test/test_data.txt")
	q = question.split(" ")
	q_vect = question_vectors(word_vector_hash, [q])[0]
	pred = model.predict(q_vect)[0]
	return pred
