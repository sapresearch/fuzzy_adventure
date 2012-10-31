import sys
sys.path.append("../")
import stanford_client as tagger
import re

class Preprocessing():

	@classmethod
	def add_tag_trees(self):
		f = file('restaurant_dataset.txt', 'r')
		with_trees = []
		for line in f:
			line = re.sub("\n", '', line)
			l = line.split(',')
			question = l[0]
			tree = tagger.to_tree(question)
			with_trees.append(line + "," + tree + "\n")
		f.close()

		f = file('rest_with_trees', 'w+')
		for w in with_trees:
			f.write(w)
		f.close()
	
	@classmethod
	def merge(self):
		f = file('geo_dataset.txt', 'r')
		for line in f:
			l = line.split(',')
			skeleton = self.to_skeleton(l[1])
		return None

	@classmethod
	def sql_tokenize(self, sql_query):
		sql_query = sql_query.split(' ')
		split_query = []
		for s in sql_query:
			if s.find('=') != -1:
				s = s.split('=')
				s.insert(1, '=')
				split_query += s
			else:
				split_query.append(s)
		split_query2 = []
		for s in split_query:
			if s.find('.') != -1:
				s = s.split('.')
				s.insert(1, '.')
				split_query2 += s
			else:
				split_query2.append(s)
		split_query3 = []
		for s in split_query2:
			if s.find('(') != -1:
				s = s.split('(')
				s.insert(1, '(')
				split = []
				for word in s:
					split += word.split(')')
				split += [')']
			else:
				split = [s]
			split_query3 += split
		if '' in split_query3:
			split_query3.remove('')

		return split_query3

	@classmethod
	def to_skeleton(self, sql_query):

		sql_query = self.sql_tokenize(sql_query)

		sql_keywords = ['delete', 'from', 'having', 'insert', 'join', 'merge', 'null', 'order by', 'select', 'union', 'update', 'where', 'count', 'distinct', 'max', 'min', 'in', 'desc', 'limit', 'sum']
		sql_syntax = ['=', '.', '(', ')', '*', '>', '<']
		skeleton = ''
		for word in sql_query:
			if word in sql_keywords:
				skeleton += word + ' '
			elif word in sql_syntax:
				skeleton += word
				if word == ')':
					skeleton += ' '
			else:
				skeleton += 'blank'
		return skeleton
	

Preprocessing.merge()
