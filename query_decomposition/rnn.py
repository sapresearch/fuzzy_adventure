""" Recursive Neural Network """
from numpy import *
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from copy import copy

rows, columns = 11, 22

class RNN():

	def __init__(self, nb_input, word_vectors, sentences, targets):
		self.nb_input = nb_input
		self.sentences = sentences
		self.targets = targets
		self.word_vectors = word_vectors
		self.theta = self.random_matrix(0.01)
		self.classifier = self.train_classifier()
	
	def train(self, pop_size=10, gen_size=10):
		best = self.cost()
		for g in range(gen_size):
			parent = copy(self.theta)
			best_theta = copy(parent)
			for i in range(pop_size):
				child = parent + self.random_matrix((1./(1+g))+0.1)
				self.theta = child
				self.classifier = self.train_classifier()
				cost = self.cost()
				if cost <= best:
					best_theta = copy(child)
					best = copy(cost)
			self.theta = best_theta
			print "Gen: " + str(g) + ". " + str(best)
		self.classifier = self.train_classifier()
		return best_theta

	def random_matrix(self, scale=1):
		mat = (random.rand(rows, columns) + (random.rand(rows, columns) * -1)) * scale
		mat = mat.round(5)
		return mat

	def activate(self, word1, word2):
		vector = array([concatenate((word1, word2), axis=1)])
		parent = inner(self.theta, vector).T
		parent = concatenate(parent, axis=1)
		norm = linalg.norm(parent)
		parent = parent/norm
		parent = parent.round(5)

		vector = concatenate(vector, axis=1)
		return parent, vector
	
	def train_classifier(self):
		vectors = []
		#limit = len(self.sentences)/5 * 4
		targets = []
		for i,s in enumerate(self.sentences):
			_, trees, _, _ = self.recursive_parse(s)
			vectors = vectors + trees

			# Get the same number of targets as input vectors.
			answer = self.targets[i]
			for x in range(len(trees)):
				targets.append(answer)
		classifier = LogisticRegression(C=1000., penalty='l2', tol=0.01)
		#vectors = [v.tolist() for v in vectors]
		classifier = classifier.fit(vectors, targets)
		return classifier
	
	def classify(self, vector):
		prediction = self.classifier.predict(vector)[0]
		return prediction
			
	def cost(self):
		correct = 0.
		total_cost = 0.
		all_parents = []
		all_kids = []
		for i,s in enumerate(self.sentences):
			answer = self.targets[i]
			_, parents, concatenated, cost = self.recursive_parse(s, answer, True)
			all_parents += parents
			all_kids += concatenated
			total_cost += cost
		reconstructor = LinearRegression()
		reconstructor = reconstructor.fit(all_parents, all_kids)
		preds = reconstructor.predict(all_parents)

		alpha = 0.75
		regularization_cost = np.mean((self.theta) ** 2) * alpha
		reconstruction_cost = np.mean((preds - all_kids) ** 2) ** 0.05
		classification_cost = total_cost/len(self.sentences)
		combined = (classification_cost + reconstruction_cost)/2.
		combined += regularization_cost
		return combined
	
#	def recursive_parse(self, sentence, answer=False, calc_cost=False):
#		sentence = sentence.split(' ')
#		vectors = []
#		for s in sentence:
#			word_vector = self.word_vectors[s] if s in self.word_vectors else zeros(rows)
#			vectors.append(word_vector)
#		
#		sentence_vector = zeros(len(vectors[0]))
#		for v in vectors:
#			sentence_vector = sentence_vector + v
#
#		cost = 1.
#		if calc_cost == True:
#			if self.classify(sentence_vector) == answer:
#				#print "Correct: " + str(answer) + " " + str(self.classify(sentence_vector))
#				cost = 0.
#
#		return [sentence_vector], [sentence_vector], cost

	def recursive_parse(self, sentence, answer=False, calc_cost=False):
		sentence = sentence.split(' ')
		vectors = []
		for s in sentence:
			word_vector = self.word_vectors[s] if s in self.word_vectors else random.rand(rows) * 0.001
			vectors.append(word_vector)
		sentence_vector, all_vectors, concatenated = self.merge(vectors, [], [])

		correct = 0.
		if calc_cost == True:
			for v in all_vectors:
				if self.classify(v) == answer:
					correct += 1.
		cost = 1. - (correct/len(all_vectors))
		return sentence_vector, all_vectors, concatenated, cost


	def merge(self, array, total=[], total_originals=[]):
		copied = []
		merged = []
	
		if len(array) == 2:
			parent, concatenated = self.activate(array[0], array[1])
			total_originals.append(concatenated)
			total.append(parent)
			merged.append(parent)
			copied.append(0)
			copied.append(1)
			
		a_index = 0
		for a,b,c in zip(array,array[1:],array[2:]):
			b_index = a_index+1
			if a_index not in copied and b_index not in copied:
				#if c in copied:
				copied.append(a_index)
				copied.append(b_index)
				parent, concatenated = self.activate(a,b)
				merged.append(parent)
				total_originals.append(concatenated)
				total.append(parent)
				#elif a+b <= b+c or a in copied:
					#if a not in copied:
						#copied.append(array.index(a))
						#merged.append(a)
					#copied.append(array.index(b))
					#copied.append(array.index(c))
					#merged.append(self.activate(b,c))
			a_index += 1
		for i,vect in enumerate(array):
			if i not in copied:
				copied.append(i)
				merged.append(vect)

		if len(merged) > 1:
			merged, total, total_originals = self.merge(merged, total, total_originals)

		return merged, total, total_originals
