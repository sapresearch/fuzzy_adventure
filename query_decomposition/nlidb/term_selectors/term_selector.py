import MySQLdb
import sys
sys.path.append("/home/I829287/fuzzy_adventure/query_decomposition/")
import combinatorial_tree
from time import time

class TermSelector():

	@classmethod
	def fill_in_the_blanks(self, sql_template, keywords):
		blanks = sql_template[1]
		template = sql_template[0]
		if blanks == 0:
			return template
		if len(keywords) < blanks:
			raise RuntimeError("There were not enough keywords provided to fill all the variables in the SQL template")
		combos = combinatorial_tree.permutations(keywords, blanks)
		all_queries = []
		for combo in combos:
			filled_query = template%combo
			all_queries.append(filled_query)
		return all_queries
	
	@classmethod
	def crash_and_burn(self, queries):
		answers = []
		db = MySQLdb.connect(host="localhost", user="root", passwd="nolwen", db="watchTower")
		for query in queries:
			try:
				db.query(query)
				result = db.store_result().fetch_row(0)[0][0]
				answers.append(result)
			except (MySQLdb.ProgrammingError,MySQLdb.OperationalError):
				pass
		db.close()
		return answers
	
	@classmethod
	def filter_answers(self, answers):
		return [a for a in answers if a > 0] 


#sql = "SELECT COUNT(transactions.id) FROM transactions WHERE transactions.end_date <>'0000-00-0000' AND transactions.programmer_id=(SELECT id FROM %s WHERE programmers.name = '%s');"

keywords = ['jeff', 'baumer', 'hello', '0100157232', 'transactions', 'mark', 'rob', 'other', 'thing', 'world', 'foo', 'bar', 'programmers']
arg = (sql, 2)

start = time()
queries = TermSelector.fill_in_the_blanks(arg, keywords)
answers = TermSelector.crash_and_burn(queries)
correct = TermSelector.filter_answers(answers)
print correct
print "Duration: " + str(time() - start)
