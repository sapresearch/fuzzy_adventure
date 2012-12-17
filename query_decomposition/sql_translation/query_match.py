""" Take a natural language query and match it to a pre-written SQL query

To use:
query = "Who is the best person on my team?"
model = QueryModel()
nl_query = NLQuery(query, model)
print nl_query.sql_query()
print nl_query.execute()

"""

import MySQLdb
import nltk
import sys
sys.path.append("../")
import word_space
from sklearn.ensemble import RandomForestClassifier

class NLQuery():

	def __init__(self, question, model):
		self.query = question
		self.model = model

	def sql_query(self):
		query = self.query
		sql = self.model.classify(query)
		return sql

	def execute(self):
		sql = self.sql_query()
		db = MySQLdb.connect(host="localhost", user="root", passwd="", db="watchTower")
		db.query(sql)
		result = db.store_result().fetch_row(0)
		db.close()
		return result

class QueryModel():

	def __init__(self):#, nl_queries, sql_queries):
		q1 = 'SELECT name, COUNT(transactions.programmer_id) FROM programmers INNER JOIN transactions ON programmers.id = transactions.programmer_id GROUP BY transactions.programmer_id ORDER BY COUNT(transactions.programmer_id) DESC LIMIT 1;'
		q2 = 'SELECT name, COUNT(transactions.component_id) FROM components INNER JOIN transactions on components.id = transactions.component_id GROUP BY transactions.component_id ORDER BY COUNT(transactions.component_id) DESC LIMIT 1;'
		nl_queries = ['Who is the most productive programmer on my team?', 'What component is contributing the most to my backlog?']
		data = self.tokenize(nl_queries)
		self.word_vectors = word_space.word_vectors(data)
		nl_queries = [self.vectorize(n) for n in data]
		sql_query = [q1, q2]
		self.model = RandomForestClassifier()
		self.model.fit(nl_queries, sql_query)

	def tokenize(self, data):
		tokens = [nltk.word_tokenize(sent)for sent in data]
		return tokens
	
	# Return the vector sum of a sentence
	def vectorize(self, sentence):
		vect = self.word_vectors.values()[0]
		zeros = vect - vect # Get a vector with the correct dimension
		for word in sentence:
			if word in self.word_vectors:
				zeros += self.word_vectors[word]
		return zeros
	
	def classify(self, question):
		tokens = nltk.word_tokenize(question)
		vector = self.vectorize(tokens)
		return self.model.predict(vector)
