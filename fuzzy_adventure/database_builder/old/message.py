import random
from configuration import *

import nltk
from nltk.corpus import brown

PROGRAMMERS = get_nb_programmers()
BUGS = get_nb_bugs()
MESSAGES = get_nb_messages()
CUSTOMERS = get_nb_customers()

corpus = [w.lower() for w in brown.words()]
corpus_bigrams = nltk.bigrams(corpus)
corpus_bigramsCFD = nltk.ConditionalFreqDist(corpus_bigrams)

class RandomMessage(object):
	count = 0
	created_messages = []
	
	def __init__(self):
		RandomMessage.count += 1
		self.id = RandomMessage.count
		self.text_body = create_random_text(random.randint(0,50)) #'Maybe generate random text with trigram from Brown Corpus'#
		self.programmer_to = random.randint(1, PROGRAMMERS)
		self.customer_from = random.randint(1, CUSTOMERS)
		self.bug_id = random.randint(1, BUGS)
		self.reply_id = random.randint(1, MESSAGES)
		RandomMessage.created_messages.append(self)
		
		
def create_random_text(length):
	# Make a copy of the corpus bigrams to have a fresh CFD at every creation
	bigramsCFD = corpus_bigramsCFD
	word = corpus[random.randint(0,len(corpus))]
	
	sentence = word.capitalize()
	for i in range(length):
		key = bigramsCFD[word].max()
		if(key == None):
			break
		
		bigramsCFD[word].pop(key)
		word = key
		if (not (word == '.' or word == ',' or word == ';' or word == ':')):
			sentence += ' '
		if(sentence[len(sentence)-2] == '.'):
			key = word.capitalize() + ' '
		sentence += key
	return sentence