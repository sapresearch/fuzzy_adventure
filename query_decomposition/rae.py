from pybrain.structure.networks.rbm import Rbm
from pybrain.unsupervised.trainers.rbm import (RbmGibbsTrainerConfig,RbmBernoulliTrainer)
from pybrain.datasets import UnsupervisedDataSet
#from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import sys
sys.path.append("../test")
from load_data import load_data
from rnn import RNN
import question_type
from numpy import *


#class WordSpace():

class RAE(object):

	def __init__(self, in_dims, out_dims):
		self.dataset = UnsupervisedDataSet(in_dims)
		cfg = RbmGibbsTrainerConfig()
		cfg.maxIter = 3
		self.model = Rbm.fromDims(in_dims, out_dims)
		self.trainer = RbmBernoulliTrainer(self.model, self.dataset, cfg)

	def add_data(self, data):
		for d in data:
			#print "about to add: " + str(len(d))
			self.dataset.addSample(d)

	def _train(self, iterations):
		for _ in xrange(iterations):
			self.trainer.train()

class SentenceRAE(RAE):

	def __init__(self, in_dims, out_dims, wordspace, text):
		super(SentenceRAE, self).__init__(in_dims, out_dims)
		#self.wordspace = {'hello':[1,0,1,0], 'world':[1,1,1,1], 'goodbye':[0,1,0,1], 'cruel':[0,0,0.5,1]}
		#self.text = "hello world.  goodbye world.hello world. goodbye cruel world."
		self.wordspace = wordspace 
		self.text = text
		self.in_dims = in_dims
	
	def train_with_pairs(self, iterations):
		word_pair_vects = []
		sentences = self.text.split('?.')
		for sentence in questions:#sentences:
			tokens = sentence.split(' ')
			tokens = [t for t in tokens if t != ' ' and t != '']
			for w1,w2 in zip(tokens, tokens[1:]):
				v1 = self.wordspace[w1] if w1 in self.wordspace else [0] * (self.in_dims/2)
				v2 = self.wordspace[w2] if w2 in self.wordspace else [0] * (self.in_dims/2)
				#if w1 not in self.wordspace:
					##print w1
					#print len(v1)
				#if w2 not in self.wordspace:
					#print w2
					#print len(v2)
				concatenated = list(v1) + list(v2)
				#print len(concatenated)
				word_pair_vects.append(concatenated)

		self.add_data(word_pair_vects)
		self._train(iterations)
	
	def train(self, iterations):
		self.train_with_pairs(iterations)
		self.train_with_all(iterations)

	def train_with_all(self, iterations):
		examples = []
		sentences = self.text.split('?.')
		sentences = [s for s in sentences if s != '']
		for sentence in questions:#sentences:
			 print sentence
			 _, concatenated = self.activate(sentence)
			 print "concat: " + str(len(concatenated))
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
			#print len(concatenated)
			parent = self.model.activate(concatenated)
			total_originals.append(concatenated)
			total.append(parent)
			#print len(parent)
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
		#print "vect: " + str(vector)
		return self.model.predict(vector)
		





def convert(classes):
	numeric = []
	keys = {'name':0, 'location':1, 'date':2, 'occupation':3, 'boolean':4}
	for t in classes:
		numeric.append(keys[t])
	return numeric

##############################
""" Preprocessing/Cleaning """
##############################

#questions, _, targets = load_data("../test/lat_data.txt")
questions, _, targets = load_data("../test/test_data.txt")
_, word_vectors = question_type.train(questions, targets)
for word,vector in word_vectors.items():
	vector = list(vector)
	word_vectors[word] = vector
numeric = convert(targets)
text = '.'.join(questions)

##############################
""" Training """
##############################
rae = SentenceRAE(40,20, word_vectors, text)
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


##############################
""" Testing """
##############################
def test(rnn):
	questions, _, targets = load_data("../test/test_data.txt")
	#questions = questions[1::2]
	#targets = targets[1::2]
	targets = convert(targets)
	correct = 0.
	for i,q in enumerate(questions):
		tree, _, _, _ = rnn.recursive_parse(q)
		pred = rnn.classify(tree[0])
		if pred == targets[i]:
			correct += 1.
			print "Correct: " + q
