import sys
sys.path.append("/home/I829287/fuzzy_adventure/query_decomposition/nlidb/template_selectors")
sys.path.append("/home/I829287/fuzzy_adventure/query_decomposition")
from bayes import Bayes
from word_space import WordSpace
from template_type import TemplateClassifier
import MySQLdb
import time
import re
sys.path.append("/home/I829287/fuzzy_adventure/test")
import load_data

""" Main executable file for the whole system.
To use it, run the demo() function to let the user input questions to
the command line, or the test() function to find the number of questions
that it correctly classifies. """

data_file = "/home/I829287/fuzzy_adventure/query_decomposition/nlidb/template_selectors/data2.txt"
def to_sql(nl_query):
	# Use Bayes classifier
	#bayes = Bayes(data_file)
	#tc = TemplateClassifier(bayes)

	# Use word space classifier
	word_space = WordSpace(data_file)
	tc = TemplateClassifier(word_space)
	sql, sql_key = tc.template(nl_query)
	return sql, sql_key

def execute(sql):
	db = MySQLdb.connect(host="localhost", user="root", passwd="nolwen", db="watchTower")
	db.query(sql)
	result = db.store_result().fetch_row(0)
	db.close()
	return result

def demo(verbose=False):
	while True:
		print "Ask a question:"
		query = raw_input()

		verbose = re.match(".*-v", query) != None
		query = re.sub("-v", '', query)

		start = time.time()
		sql, key = to_sql(query)
		answer = execute(sql)
		duration = time.time() - start

		if verbose:
			print "Time: " + str(round(duration, 3))
			print "SQL: " + str(sql)
		print "Answer: " + str(answer) + "\n"
	return None

def test():
	text, _, targets = load_data.load_data(data_file)
	text, targets = text[0::2], targets[0::2]
	correct = 0.
	for i,t in enumerate(text):
		target = targets[i]
		sql, key = to_sql(t)
		if key == target:
			correct += 1.
	print "Accuracy: " + str(correct/len(text))		
	print "Total tested: " + str(len(text))

#demo()
test()
