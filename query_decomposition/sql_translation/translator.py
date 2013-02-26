from query_classifier import QueryClassifier
from term_selector import TermSelector

""" This is the main class for the SQL translation folder.
It takes as input a string of a natural language question.
It sends the question to the QueryClassifier, which outputs
an SQL template. This template plus the natural language
question is sent to the TermSelector, which fills in the 
blanks of the SQL template. After the blanks in the SQL
template have been filled in is the final output. """

class Translator():

	@classmethod
	def translate(self, query):
		sql_skeleton = QueryClassifier.classify(query)
		sql_query = TermSelector.fill_in_blanks(query, sql_skeleton)
		return sql_query

#print Translator.translate("what state has the highest population")
print Translator.translate("Who is the most productive programmer on my team?")
print "\n"
#print Translator.translate("what is the capital of VARstate")
print Translator.translate("What component is contributing the most to my backlog?")
print "\n"
#print Translator.translate("what river is in VARcountry")
