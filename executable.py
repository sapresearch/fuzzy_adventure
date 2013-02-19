import sys
sys.path.append("/home/I829287/fuzzy_adventure/query_decomposition")
sys.path.append("/home/I829287/fuzzy_adventure/query_decomposition/nlidb/template_selectors")
sys.path.append("/home/I829287/fuzzy_adventure/query_decomposition/nlidb/term_selectors")
sys.path.append("/home/I829287/fuzzy_adventure/query_decomposition/nlp_system")
from bayes import Bayes
from word_space import WordSpace
from template_type import TemplateClassifier
import MySQLdb
import time
import re
sys.path.append("/home/I829287/fuzzy_adventure/test")
import load_data
import confidence_estimator
from term_selector import TermSelector
import nlp
import nlp_nlidb

""" Main executable file for the whole system.
To use it, run the FuzzyAdventure.demo() function to let the user input questions to
the command line, or the FuzzyAdventure.test() function to find the number of questions
that it correctly classifies. """


#data_file = "/home/I829287/fuzzy_adventure/query_decomposition/nlidb/template_selectors/data2.txt"
data_file = "/home/I829287/fuzzy_adventure/query_decomposition/nlidb/template_selectors/more.txt"
	
# Use Bayes classifier
bayes = Bayes(data_file)
tc = TemplateClassifier(bayes)

# Use word space classifier
#word_space = WordSpace(data_file)
#tc = TemplateClassifier(word_space)

class FuzzyAdventure():

	@classmethod
	def to_sql(self, nl_query):
		supplemented = nlp_nlidb.nlp_nlidb(nl_query)
		print supplemented 
		sql, lat_type = tc.template(supplemented)
		keywords = nlp.tokens(nl_query)
		keywords = nlp.remove_stopwords(keywords)
		answer = TermSelector.fill_in_the_blanks(sql, keywords)
		return answer, lat_type

	@classmethod
	def demo(self, verbose=False):
		while True:
			print "Ask a question:"
			query = raw_input()
	
			verbose = re.match(".*-v", query) != None
			query = re.sub("-v", '', query)
	
			start = time.time()
			answer, lat_type = self.to_sql(query)
			#sql = sql[0]
			#answer = execute(sql)
			confidence = confidence_estimator.LAT_match(answer, lat_type)
			duration = time.time() - start
	
			if verbose:
				print "Time: " + str(round(duration, 3))
				#print "SQL: " + str(sql)
				print "LAT Type: " + str(lat_type)
				print "Confidence: " + str(confidence)
			print "Answer: " + str(answer) + "\n"
		return None
	
	@classmethod
	def test(self):
		data_file = "/home/I829287/fuzzy_adventure/query_decomposition/nlidb/template_selectors/data2.txt"
		text, _, targets = load_data.load_data(data_file)
		text, targets = text[1::2], targets[1::2]
		correct = 0.
		for i,t in enumerate(text):
			target = targets[i]
			sql, key = self.to_sql(t)
			print "Question: ", t
			print "Predicted/target: ", key, target
			if key == target:
				correct += 1.
		print "Accuracy: " + str(correct/len(text))		
		print "Total tested: " + str(len(text))
	
#q = "Who is my best employee?"
FuzzyAdventure.test()
