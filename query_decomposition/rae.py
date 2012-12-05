from pybrain.structure.networks.rbm import Rbm
from pybrain.unsupervised.trainers.rbm import (RbmGibbsTrainerConfig,RbmBernoulliTrainer)
from pybrain.datasets import UnsupervisedDataSet
from sklearn.ensemble import RandomForestClassifier
import sys
sys.path.append("../test")
from load_data import load_data
from rnn import RNN
import question_type
from numpy import *


class RAE(object):

	def __init__(self, in_dims, out_dims):
		self.dataset = UnsupervisedDataSet(in_dims)
		cfg = RbmGibbsTrainerConfig()
		cfg.maxIter = 3
		self.model = Rbm.fromDims(in_dims, out_dims)
		self.trainer = RbmBernoulliTrainer(self.model, self.dataset, cfg)

	def add_data(self, data):
		for d in data:
			self.dataset.addSample(d)

	def _train(self, iterations):
		for _ in xrange(iterations):
			self.trainer.train()

class SentenceRAE(RAE):

	def __init__(self, in_dims, out_dims, wordspace, text):
		super(SentenceRAE, self).__init__(in_dims, out_dims)
		self.wordspace = wordspace 
		self.text = text
		self.in_dims = in_dims
	
	def train_with_pairs(self, iterations):
		word_pair_vects = []
		for sentence in self.text:
			tokens = sentence.split(' ')
			tokens = [t for t in tokens if t != ' ' and t != '']
			for w1,w2 in zip(tokens, tokens[1:]):
				v1 = self.wordspace[w1] if w1 in self.wordspace else [0] * (self.in_dims/2)
				v2 = self.wordspace[w2] if w2 in self.wordspace else [0] * (self.in_dims/2)
				concatenated = list(v1) + list(v2)
				word_pair_vects.append(concatenated)
		self.add_data(word_pair_vects)
		self._train(iterations)
	
	def train(self, iterations):
		self.train_with_pairs(iterations)
		self.train_with_all(iterations)

	def train_with_all(self, iterations):
		examples = []
		for sentence in self.text:
			 _, concatenated = self.activate(sentence)
			 examples.append(concatenated)
		self.add_data(examples)
		self._train(iterations)
	
	def activate(self, sentence):
		tokens = sentence.split(' ')
		tokens = [t for t in tokens if t != ' ' and t != '']
		vectors = []
		for s in tokens:
			word_vector = self.wordspace[s] if s in self.wordspace else [0.001] * self.in_dims
			vectors.append(word_vector)
		sentence_vector, all_vectors, concatenated = self.merge(vectors, [], [])
		return sentence_vector[0], concatenated[0]

	def merge(self, array, total=[], total_originals=[]):
		copied = []
		merged = []
	
		if len(array) == 2:
			concatenated = list(array[0]) + list(array[1])
			parent = self.model.activate(concatenated)
			total_originals.append(concatenated)
			total.append(parent)
			merged.append(parent)
			copied.append(0)
			copied.append(1)
			
		a_index = 0
		for a,b,c in zip(array,array[1:],array[2:]):
			b_index = a_index+1
			if a_index not in copied and b_index not in copied:
				copied.append(a_index)
				copied.append(b_index)
				concatenated = list(array[0]) + list(array[1])
				parent = self.model.activate(concatenated)
				merged.append(parent)
				total_originals.append(concatenated)
				total.append(parent)
			a_index += 1
		for i,vect in enumerate(array):
			if i not in copied:
				copied.append(i)
				merged.append(vect)

		if len(merged) > 1:
			merged, total, total_originals = self.merge(merged, total, total_originals)

		return merged, total, total_originals

class RAEClassifier():

	def __init__(self, rae, data, targets):
		self.model = RandomForestClassifier(n_estimators=5)
		self.rae = rae
		self.targets = targets
		self.data = data
		self.train()

	def train(self):
		_data = []
		for item in self.data:
			vector, _ = self.rae.activate(item)
			_data.append(vector)
		m = self.model
		m.fit(_data, targets)
		self.model = m

	def predict(self, item):
		vector, _ = self.rae.activate(item)
		return self.model.predict(vector)
		




questions, _, targets = load_data("../test/test_data.txt")
_, word_vectors = question_type.train(questions, targets)
for word,vector in word_vectors.items():
	vector = list(vector)
	word_vectors[word] = vector

rae = SentenceRAE(40,20, word_vectors, questions)
rae.train(0)


cls = RAEClassifier(rae, questions, targets)
print cls
print questions[5]
print cls.predict(questions[5])
print questions[15]
print cls.predict(questions[15])
print questions[25]
print cls.predict(questions[25])
print questions[35]
print cls.predict(questions[35])
print questions[45]
print cls.predict(questions[45])
