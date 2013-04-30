from fuzzy_adventure.query_decomposition.nlp_system import stanford_client as tagger
import re
import pandas as pd
from pandas import DataFrame, Series

class Preprocessing():

	@classmethod
	def data(self):
		originals, skeletons, trees = self.generalize_sql()
		unique = list(set(skeletons))
		labels = []
		cleaned_trees = []
		for tree in trees:
			cleaned_trees.append(self.format_trees(tree))

		df = count(cleaned_trees, skeletons)
		print df.ix[0]

		for i,sql in enumerate(originals):
			skeleton = skeletons[i]
			label = unique.index(skeleton) # Label every original sql with its skeleton
			labels.append(label)
		return originals, labels, cleaned_trees


	@classmethod
	def generalize_sql(self):
		f = file('IMS_questions.txt', 'r') # To change the training dataset, change this file here.
		originals = []
		skeletons = []
		trees = []
		for line in f:
			line = line.split(',')

			sql = line[1]
			originals.append(sql)

			skeleton = self.to_skeleton(sql)
			skeletons.append(skeleton)

			parse_tree = line[2]
			trees.append(parse_tree)

		f.close()
		return originals, skeletons, trees


	@classmethod
	def format_trees(self, tree):
		tags_only = re.sub("[^A-Z+]", " ", tree)
		clean = re.sub("\s+", ' ', tags_only)
		clean = re.sub("^\s", '', clean)
		clean = re.sub("\s$", '', clean)
		return clean


	@classmethod
	def to_skeleton(self, sql_query):
		sql_query = self.sql_tokenize(sql_query)

		sql_keywords = ['delete', 'from', 'having', 'insert', 'join', 'merge', 'null', 'order by', 'select', 'union', 'update', 'where', 'count', 'distinct', 'max', 'min', 'in', 'desc', 'limit', 'sum', 'and', 'or']
		sql_syntax = ['=', '.', '(', ')', '*', '>', '<']
		skeleton = ''
		for word in sql_query:
			if word != '':
				if word in sql_keywords:
					skeleton += word + ' '
				elif word in sql_syntax:
					skeleton += word + ' '
				else:
					skeleton += 'blank' + ' '
		skeleton = re.sub(" \. ", '.', skeleton)
		skeleton = re.sub(" = ", '=', skeleton)
		skeleton = re.sub("\( ", "(", skeleton)
		skeleton = re.sub(" \)", ")", skeleton)
		skeleton = re.sub("max \(", "max(", skeleton)
		skeleton = re.sub("min \(", "min(", skeleton)
		skeleton = re.sub("sum \(", "sum(", skeleton)
		skeleton = re.sub("count \(", "count(", skeleton)
		return skeleton


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
				split_query3 += s
			else:
				split_query3.append(s)

		split_query4 = []
		for s in split_query3:
			if s.find(')') != -1:
				s = s.split(')')
				s.insert(1, ')')
				split_query4 += s
			else:
				split_query4.append(s)

		if '' in split_query4:
			split_query4.remove('')
		return split_query4


	" This method was to create the dataset. It's not used anymore. "
	@classmethod
	def add_tag_trees(self):
		f = file('geo_dataset.txt', 'r')
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
	def query(self, query_label):
		originals, skeletons, trees = self.generalize_sql()
		unique = list(set(skeletons))
		labels = []
		query = unique[query_label]
		return query
	


def count(trees, sql):
    df = DataFrame(zip(trees, sql), columns=['tree','sql'])
    gb = df.groupby(['tree','sql'])

    c = []
    for k in gb.groups.keys():
        l = (len(gb.groups[k]),)
        c.append(k + l)

    df = DataFrame(c)
    df.index = [df[0], df[1]]
    del df[0]
    del df[1]
    df.columns = ['count']
    df.index.names = ['tree','sql']
    return df
