from query_classifier import QueryClassifier
from term_selector import TermSelector

class Translator():

	@classmethod
	def translate(self, query):
		sql_skeleton = QueryClassifier.classify(query)
		sql_query = TermSelector.fill_in_blanks(query, sql_skeleton)
		return sql_query

print Translator.translate("what state has the highest population")
print "\n"
print Translator.translate("what is the capital of VARstate")
print "\n"
print Translator.translate("what river is in VARcountry")
