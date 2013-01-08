from numpy import *
from random import shuffle
from numpy.linalg import norm
import nltk
from nltk import *
from sklearn import tree
from sklearn.ensemble import ExtraTreesClassifier
import sys
sys.path.append("/home/I829287/fuzzy_adventure/test")
import load_data
import time

zero = 98
one = 1
length = zero + one + one # for both positive an dnegative count.

def random_vector(zero, one):
	z = zeros(zero)
	positives = ones(one)
	negatives = ones(one) * -1
	merged = array(list(z) + list(positives) + list(negatives))
	shuffle(merged)
	return merged

def empty_vectors(words):
	words = set(words) # unique them
	dict = {}
	for w in words:
		dict[w] = zeros(length)
	return dict

""" Takes as input a multidimensional array
with a subarray for each section of the corpus:
[['hello' 'world'], ['goodbye', 'world']]
It returns a dictionary of each word to its vector. """
def word_vectors(corpus):
	count = 0
	all_words = []
	for section in corpus:
		all_words += section
	vectors = empty_vectors(all_words)
	for line in corpus:
		context_vector = random_vector(zero, one)
		for word in line:
			vectors[word] += context_vector

	# Normalize them.
	for word,vect in vectors.items():
		norm = linalg.norm(vect)
		vectors[word] = (vect/norm).round(2)
	return vectors

def cosine(v1,v2):
	return float(dot(v1,v2) / (norm(v1) * norm(v2)))


def load_cosines(file_name):
	f = open(file_name, 'r')
	lines = f.readlines()
	dict = {}
	for line in lines:
		line = line.split(',')
		word = line.pop(0)
		vector = []
		for e in line:
			vector.append(int(e))
		dict[word] = array(vector)
	return dict

def save_cosines(vectors, file_name):
	f = open(file_name, 'w')
	for k,v in vectors.items():
		f.write(k + str(v).strip('[]') + "\n")
	f.close


class WordSpace():

	def __init__(self, file_path, vector_length=100):
		self.file_path = file_path
		self.vector_length = vector_length
	
	def train(self, questions, types):
		question_arrays = []
		for q in questions:
			question_arrays.append(q.split(" "))
	
		word_vector_hash = word_vectors(question_arrays)
		questions = self.question_vectors(word_vector_hash, question_arrays)
	
		xtrees = ExtraTreesClassifier(n_estimators=10, max_depth=None, min_samples_split=1, random_state=0)
		model = xtrees.fit(questions, types)
		return model, word_vector_hash
	
	def question_vectors(self, word_vector_hash, questions):
		question_vectors = []
		for q in questions:
			vect = zeros(self.vector_length)
			for word in q:
				if word in word_vector_hash:
					vect += word_vector_hash[word]
			question_vectors.append(vect)
		return question_vectors
	
	def hardcode(self, query):
		return None

	def classify(self, query, model=None, word_vector_hash=None):
		pred = self.hardcode(query)
		if pred != None:
			return pred
		if model == None or word_vector_hash == None:
			questions, _, types = load_data.load_data(self.file_path)
			model, word_vector_hash = self.train(questions, types)
		q = query.split(" ")
		q_vect = self.question_vectors(word_vector_hash, [q])[0]
		pred = model.predict(q_vect)[0]
		return pred
