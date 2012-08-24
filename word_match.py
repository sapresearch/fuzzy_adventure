from numpy import *
from random import shuffle
from numpy.linalg import norm
import nltk
from nltk import *
import time

zero = 8
one = 1
length = zero + one + one

def random_vector(zero, one, negative):
	z = zeros(zero)
	positives = ones(one)
	if negative == True:
		negatives = ones(one) - 2
		merged = array(list(z) + list(positives) + list(negatives))
	elif negative == False:
		merged = array(list(z) + list(positives) + list(positives))
	shuffle(merged)
	return merged

def empty_vectors(words):
	words = set(words) # unique them
	dict = {}
	for w in words:
		dict[w] = zeros(length)
	return dict

def word_vectors(corpus, negative):
	count = 0
	dict = empty_vectors(corpus)
	for word in corpus:
		if count % 10 == 0:
			context_vector = random_vector(zero, one, negative)
		dict[word] += context_vector
		count += 1
	return dict

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
corpus = nltk.Text(word.lower() for word in nltk.corpus.brown.words())
corpus = corpus.tokens[0:100]
#start = time.time()
dict = word_vectors(corpus, True)
save_cosines(dict, 'y.txt')
#print time.time() - start
#print cosine(dict['fly'], dict['pen'])
#print cosine(dict['born'], dict['birth'])
#print cosine(dict['man'], dict['woman'])
#print cosine(dict['girl'], dict['woman'])
#print cosine(dict['man'], dict['work'])
