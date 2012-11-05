#from nltk import stopwords#as stopwords
from nltk.corpus import stopwords
from nltk.metrics import edit_distance
import re

class TermSelector():

	@classmethod
	def table_names(self):
		tables = ['state', 'city', 'border_info', 'highlow', 'river', 'mountain']
		return tables

	@classmethod
	def column_names(self):
		columns = ['capital', 'population', 'city_name', 'state_name', 'area', 'country_name', 'border', 'highest_point', 'density', 'highest_elevation', 'length']
		return columns

	@classmethod
	def row_names(self):
		rows = ['VARstate', 'VARcountry']
		return rows

	@classmethod
	def format_sql(self, sql):
		print sql + "'"
		sql = re.sub("\w*\.", 'table.', sql)
		sql = re.sub("from blank", 'from table', sql)
		sql = re.sub("\.\w*", '.column', sql)
		sql = re.sub("=blank\s?$", '=row', sql)
		print sql
		return sql
	
	@classmethod
	def fill_in_blanks(self, question, sql_query):
		print question
		db_names = self.select_names(question)
		query = self.format_sql(sql_query)
		for name in db_names:
			if name in self.table_names():
				query = re.sub("table", name, query)
			elif name in self.column_names():
				query = re.sub("column", name, query)
			elif name in self.row_names():
				query = re.sub("row", name, query)
		return query
	
	@classmethod
	def select_names(self, question):
		words = question.split(' ')
		filtered = [w for w in words if not w in stopwords.words('english')]
		print filtered
		db_names = [self.similar(f) for f in filtered]
		db_names = set(db_names)
		print db_names
		return db_names	
		
	@classmethod
	def similar(self, word):
		names = self.table_names() + self.column_names() + self.row_names()
		best = 100
		best_word = None
		for name in names:
			dist = edit_distance(name, word)
			if dist <= best:
				best,best_word = dist,name
				#print "Best word: " + best_word + " for " + word + ". Distance: " + str(dist)
		return best_word

#print TermSelector.fill_in_blanks('what is the state_name of the state has the highest population', "select blank.blank from blank where blank.blank=(select max(blank.blank) from blank)" )
#answer = "select state.state_name from state where state.population=(select max(state.population) from state)"
#print answer
		
		
		
"""
	1. remove stopwords
	2. find each blank in sql query and match it with a table or a column
	3. find the specific table/column
	4. go to each non-stopword and find which column/table name it is most similiar to.  Then select the best candidates
	5. find table-column pairs and generate all the possibilities
"""
