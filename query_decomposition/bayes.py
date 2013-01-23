import nlp
from sklearn.naive_bayes import GaussianNB
import sys
sys.path.append("/home/I834397/Git/fuzzy_adventure/test")
import load_data

class Bayes():

	def __init__(self, file_path):
		self.file_path = file_path
		self.word_list = self.build_word_list
		self.model = self.train()
	
	""" Create an alphabetized wordlist of all the words in all classes """
	def build_word_list(self):
		text, _, _ = load_data.load_data(self.file_path)
		text = text[1::2]
		text = [nlp.tokens(t) for t in text]
		text = [word for sentence in text for word in sentence]
		text = list(set(text))
		text.sort()
		return text
	
	""" Takes a string as input and returns a vector of 1's and 2's.
	Uses Laplace smoothing to create a vector for the text. """
	def text_vector(self, text):
		text = nlp.tokens(text)
		vector = []
		for word in self.word_list():
			score = 2 if word in text else 1
			vector.append(score)
		return vector
	
	def train(self):
		texts, _, targets = load_data.load_data(self.file_path)
		data = []
		for t in texts:
			vector = self.text_vector(t)
			data.append(vector)
		model = GaussianNB()
		model.fit(data, targets)
		return model
	
	def classify(self, text):
		vector = self.text_vector(text)
		return self.model.predict(vector)[0]
