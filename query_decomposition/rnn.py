""" Recursive Neural Network """
from numpy import *
from sklearn.ensemble import ExtraTreesClassifier
from copy import copy

rows, columns = 2, 4

class RNN():

	def __init__(self, nb_input, sentences, targets):
		self.nb_input = nb_input
		self.sentences = sentences
		self.targets = targets
		self.word_vectors = { 'hello':array([1,2]), 'world':array([5,5]), 'goodbye':array([4,4]) }
		self.theta = matrix([[1,1,1,1],[1,1,1,1]])
		#self.theta = random.rand(rows, columns)
		self.classifier = None
	
	def train(self):
		original = copy(self.theta)
		pop_size = 5
		best, best_theta = self.cost(), original
		for i in range(pop_size):
			child = original + self.random_matrix()
			self.theta = child
			cost = self.cost()
			print "Cost: " + str(cost)
			print "Child: " + str(child)
			if cost < best:
				best_theta = child
				best = cost
		self.theta = best_theta
		return best_theta

	def random_matrix(self):
		mat = (random.rand(rows, columns) * 2) + (random.rand(rows, columns) * -2)
		return mat

	def activate(self, word1, word2):
		vector = array([concatenate((word1, word2), axis=1)])
		print self.theta
		print vector.T
		parent = (self.theta * vector.T).T
		parent = concatenate(parent, axis=1)
		return parent
	
	def parse(self, sentence):
		sentence = sentence.split(' ')
		parent_vector = self.word_vectors[sentence[0]]
		for s in sentence[1:]:
			word2_vector = self.word_vectors[s]
			parent_vector = self.activate(parent_vector, word2_vector)
		return parent_vector
	
	def train_classifier(self):
		vectors = []
		for s in self.sentences:
			tree = self.parse(s)
			vectors.append(tree)
		classifier = ExtraTreesClassifier(n_estimators=1, max_depth=None, min_samples_split=1, random_state=0)
		vectors = [v.tolist()[0] for v in vectors]
		classifier = classifier.fit(vectors, self.targets)
		self.classifier = classifier
	
	def classify(self, sentence):
		tree = self.parse(sentence)
		prediction = self.classifier.predict(tree)
		return prediction
			
	def cost(self):
		correct = 0.
		for i,s in enumerate(self.sentences):
			answer = self.targets[i]
			if self.classify(s) == answer:
				correct += 1.
		accuracy = correct/len(self.targets)
		return 1.0 - accuracy
