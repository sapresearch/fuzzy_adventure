from numpy import *
from random import shuffle
from numpy.linalg import norm
import nltk
from nltk import *
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


#corpus = ['hey', 'there', 'how', 'are', 'you', 'i', 'am', 'good', 'but', 'it', 'is', 'raining', 'there']
#corpus = nltk.Text(word.lower() for word in nltk.corpus.brown.words())
#corpus = corpus.tokens[0:100]
#start = time.time()
#dict = word_vectors(corpus, True)
#save_cosines(dict, 'y.txt')
#print time.time() - start
#print cosine(dict['fly'], dict['pen'])
#print cosine(dict['born'], dict['birth'])
#print cosine(dict['man'], dict['woman'])
#print cosine(dict['girl'], dict['woman'])
#print cosine(dict['man'], dict['work'])
