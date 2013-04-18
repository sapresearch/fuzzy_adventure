from pybrain.structure.networks.rbm import Rbm
from pybrain.unsupervised.trainers.rbm import (RbmGibbsTrainerConfig,RbmBernoulliTrainer)
from pybrain.datasets import UnsupervisedDataSet
from sklearn.ensemble import RandomForestClassifier
from fuzzy_adventure.test.load_data import load_data
from rnn import RNN
import question_type
from numpy import *
import time


class RAE(object):

	def __init__(self, in_dims, out_dims):
		self.dataset = UnsupervisedDataSet(in_dims)
		cfg = RbmGibbsTrainerConfig()
		cfg.maxIter = 5
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
		self.train_with_pairs(5)
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
			word_vector = self.wordspace[s] if s in self.wordspace else [0.001] * (self.in_dims/2)
			vectors.append(word_vector)
		sentence_vector, all_vectors, concatenated = self.merge(vectors, [], [])
		#print sentence_vector
		if len(sentence_vector) == 0 or len(concatenated) == 0:
			print "'" + sentence + "'"
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
		
	def test(self, test_data, test_targets):
		preds = []
		for q in test_data:
			preds.append(self.predict(q)[0])
		index = range(len(test_data))
		correct = 0.
		for i in index:
			pred = preds[i]
			target = test_targets[i]
			correct = correct + 1. if pred == target else correct
		print "Correct: " + str(correct/float(len(test_targets)))



import nltk
brown = nltk.corpus.brown

sents = brown.sents()
formatted = []
dummy_targets = [] # So that the question_type.train function doesn't complain when it tries to train a RandomForest.
for s in sents[0:500]:
	s = [token for token in s if token not in ['?', ',', '.', '(', ')']]
	if len(s) > 1:
		sent = ' '.join(s)
		formatted.append(sent)
		dummy_targets.append('a')
brown = formatted
print "Training sentences: " + str(len(brown))
#brown = ' '.join(brown)
#brown = brown.split('. ')
#brown = [s for s in brown if s != ' ' and s != '' and len(s) > 11]

questions, _, targets = load_data("../test/lat_data.txt") # training 
test_questions, _, test_targets = load_data("../test/test_data.txt")# cross validaiotn
questions = [q.strip('?') for q in questions]
test_questions = [q.strip('?') for q in test_questions]

#_, word_vectors = question_type.train(questions, targets)
_, word_vectors = question_type.train(brown, dummy_targets)
for word,vector in word_vectors.items():
	vector = list(vector)
	word_vectors[word] = vector


rae = SentenceRAE(200,100, word_vectors, brown)
epochs = 10
rae.train(1)
for i in range(epochs):
	start = time.time()
	
	cls1 = RAEClassifier(rae, questions, targets)
	cls2 = RAEClassifier(rae, test_questions, test_targets)
	
	print "Epochs: " + str(i+1) + "\n"
	print "Classifier trained on training data"
	cls1.test(questions, targets)
	cls1.test(test_questions, test_targets)
	
	print "\nClassifier trained on cv data"
	cls2.test(questions, targets)
	cls2.test(test_questions, test_targets)

	rae._train(1)
	print "Time: " + str(time.time() - start) + "\n"




#print questions[5]
#print cls.predict(questions[5])
#print questions[15]
#print cls.predict(questions[15])
#print questions[25]
#print cls.predict(questions[25])
#print questions[35]
#print cls.predict(questions[35])
#print questions[45]
#print cls.predict(questions[45])
