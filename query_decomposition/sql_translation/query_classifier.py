from preprocessing import Preprocessing
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
import numpy as np
import sys
sys.path.append("../")
import stanford_client as tagger

class FeatureExtraction():

	@classmethod
	def tree_ngrams(self, trees):
		ngrams = []
		for t in trees:
			t = t.split(' ')
			ngrams.append(self.ngrams(2, t))
		return ngrams

	@classmethod
	def ngrams(self, n, sentence):
		grams = []
		word_count = range(len(sentence) - (n-1))
		for word in word_count:
			start = word
			stop = word + n
			gram = ' '.join(sentence[start:stop])
			grams.append(gram)
		return grams

class QueryClassifier():

	@classmethod
	def classify(self, nl_query):
		pos_tree = tagger.to_tree(nl_query)
		_, labels, trees = Preprocessing.data()
		text_clf = Pipeline([ ('vect', CountVectorizer(min_n=1, max_n=1)), ('tfidf', TfidfTransformer(use_idf=False)), ('clf', LinearSVC()) ])
		_ = text_clf.fit(trees, labels)
		predicted = text_clf.predict([pos_tree])[0]
		predicted = Preprocessing.query(predicted)
		return predicted
	
	@classmethod
	def test(self):
		_, labels, trees = Preprocessing.data()
		test_labels = labels[2::3]
		test_trees = trees[2::3]
		labels = labels[0::3] + labels[1::3]
		trees = trees[0::3] + trees[1::3]
		#text_clf = Pipeline([ ('vect', CountVectorizer(min_n=2, max_n=3)), ('tfidf', TfidfTransformer(use_idf=False)), ('clf', MultinomialNB()) ])
		text_clf = Pipeline([ ('vect', CountVectorizer(min_n=1, max_n=1)), ('tfidf', TfidfTransformer(use_idf=False)), ('clf', LinearSVC()) ])
		_ = text_clf.fit(trees, labels)
		predicted = text_clf.predict(test_trees)
		accuracy = np.mean(predicted == test_labels)
		return accuracy

#print "----"
#print QueryClassifier.test()
#print QueryClassifier.classify("What states border Florida?")
