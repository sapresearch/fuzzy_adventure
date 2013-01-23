""" Uses the Decorator design pattern. This class wraps another class and adds the .template function to that class.
This .template function just allows us to put an 'A' or 'B' in the data file, rather than the long SQL statement that
the line corresponds with.  This way, we can change the SQL statement without modifying each example in the training file.
To use this, the class accepts an instance of another class at initialization:

bayes = Bayes(data_file)
classifier = TemplateClassifier(bayes)
classifier.tempate(query)

I don't want the Bayes class or the WordSpace class to inherit this function from a superclass, because I'll use them
in other modules where this function isn't necessary. """

import sys
sys.path.append("~/fuzzy_adventure/query_decomposition")
from confidence_estimator import *
class TemplateClassifier():

	q1 = ("SELECT name, COUNT(transactions.programmer_id) AS close_count FROM programmers, transactions WHERE programmers.id = transactions.programmer_id AND programmers.name <>'' GROUP BY transactions.programmer_id ORDER BY close_count DESC LIMIT 1;", 0)
	q2 = ('SELECT name, COUNT(transactions.component_id) FROM components INNER JOIN transactions on components.id = transactions.component_id GROUP BY transactions.component_id ORDER BY COUNT(transactions.component_id) DESC LIMIT 1;', 0)
	q3 = ("SELECT COUNT(transactions.id) FROM transactions WHERE transactions.end_date <>'0000-00-0000' AND transactions.programmer_id=(SELECT id FROM programmers WHERE programmers.name = '%s');", 1)
	templates = {'A': [q1, LAT.Programmer], 'B': [q2, LAT.Component], 'C': [q3, LAT.Integer]}

	def __init__(self, model):
		self.model = model
	
	def template(self, query):
		klass = self.model.classify(query)
		klass = 'C'
		sql = self.templates[klass][0]
		lat_type = self.templates[klass][1]
		return sql, lat_type
