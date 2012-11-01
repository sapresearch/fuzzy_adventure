import sys
sys.path.append("../")
import stanford_client as tagger
import re

class Preprocessing():

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
	def generalize_sql(self):
		f = file('geo_dataset.txt', 'r')
		originals = []
		skeletons = []
		trees = []
		for line in f:
			line = line.split(',')
			sql = line[1]
			parse_tree = line[2]
			skeleton = self.to_skeleton(sql)
			trees.append(parse_tree)
			originals.append(sql)
			skeletons.append(skeleton)
		f.close()
		return originals, skeletons, trees

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

	@classmethod
	def to_skeleton(self, sql_query):
		sql_query = self.sql_tokenize(sql_query)

		sql_keywords = ['delete', 'from', 'having', 'insert', 'join', 'merge', 'null', 'order by', 'select', 'union', 'update', 'where', 'count', 'distinct', 'max', 'min', 'in', 'desc', 'limit', 'sum']
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
	def data(self):
		originals, skeletons, trees = self.generalize_sql()
		unique = list(set(skeletons))
		labels = []
		cleaned_trees = []
		for tree in trees:
			cleaned_trees.append(self.format_trees(tree))
		for i,sql in enumerate(originals):
			skeleton = skeletons[i]
			label = unique.index(skeleton)
			labels.append(label)
		return originals, labels, cleaned_trees
	
	@classmethod
	def format_trees(self, tree):
		tags_only = re.sub("[^A-Z+]", " ", tree)
		clean = re.sub("\s+", ' ', tags_only)
		clean = re.sub("^\s", '', clean)
		clean = re.sub("\s$", '', clean)
		return clean
