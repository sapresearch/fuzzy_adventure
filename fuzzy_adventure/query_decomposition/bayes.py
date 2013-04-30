import nlp
from sklearn.naive_bayes import GaussianNB
from fuzzy_adventure.test import load_data

class Bayes():

	def __init__(self, file_path):
		self.file_path = file_path
		self.word_list = self.build_word_list()
		self.model = self.fit()
	
	""" Create an alphabetized wordlist of all the words in all classes """
	def build_word_list(self):
		text, _ = load_data.load_questions(self.file_path)
		text = text[0::2]
		text = [nlp.tokens(t) for t in text]
		text = [word for sentence in text for word in sentence]
		text = list(set(text))
		text.sort()
		return text
	
	""" Takes a string as input and returns a vector of 1's and 2's.
	Uses Laplace smoothing to create a vector for the text. """
	def text_vector(self, text, laplace):
		text = nlp.tokens(text)
		vector = []
		for word in self.word_list:
			score = 1 if word in text else 0
			vector.append(score)
		return vector
	
	def fit(self):
		texts, targets = load_data.load_questions(self.file_path)
		data = []
		for t in texts:
			vector = self.text_vector(t, False)
			data.append(vector)
		model = GaussianNB()
		model.fit(data, targets)
		return model
	
	def predict(self, text):
		vector = self.text_vector(text, True)
		return self.model.predict(vector)[0]
