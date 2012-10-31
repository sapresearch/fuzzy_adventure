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
		return None
	

Preprocessing.add_tag_trees()
