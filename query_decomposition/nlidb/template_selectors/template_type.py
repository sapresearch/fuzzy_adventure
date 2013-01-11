""" Uses the Decorator design pattern. This class wraps another class and adds the .template function to that class.
This .template function just allows us to put an 'A' or 'B' in the data file, rather than the long SQL statement that
the line corresponds with.  This way, we can change the SQL statement without modifying each example in the training file.
To use this, the class accepts an instance of another class at initialization:

bayes = Bayes(data_file)
classifier = TemplateClassifier(bayes)
classifier.tempate(query)

I don't want the Bayes class or the WordSpace class to inherit this function from a superclass, because I'll use them
in other modules where this function isn't necessary. """

class TemplateClassifier():

	q1 = 'SELECT name, COUNT(transactions.programmer_id) FROM programmers INNER JOIN transactions ON programmers.id = transactions.programmer_id GROUP BY transactions.programmer_id ORDER BY COUNT(transactions.programmer_id) DESC LIMIT 1;'
	q2 = 'SELECT name, COUNT(transactions.component_id) FROM components INNER JOIN transactions on components.id = transactions.component_id GROUP BY transactions.component_id ORDER BY COUNT(transactions.component_id) DESC LIMIT 1;'
	templates = {'A': q1, 'B': q2}

	def __init__(self, model):
		self.model = model
	
	def template(self, query):
		klass = self.model.classify(query)
		print klass
		sql = self.templates[klass]
		return sql, klass
