import copy
import re

class StanfordNode():
    
    def __init__(self, node_type='ROOT', word=None, probability=0.0, children=[], parent=None):
        self.node_type = node_type
        self.word = word
        self.probability = probability
        self.children = children
        self.parent = parent


        
def parse(tree, parent=None, root_node=None, count=0, debug=False):
	length = len(tree)
	start_count, stop_count = 0, 0
	sub_start, sub_stop = 0, 0

	next_section = ''
	next_sections = []
	for letter in tree:

		if letter == '(':
			start_count += 1
			sub_start += 1
			if start_count == 2:
				sub_start = 1
				sub_stop = 0
		elif letter == ')':
			stop_count += 1
			sub_stop += 1

		if sub_start == sub_stop and start_count > 0:
			sub_start = 0
			sub_stop = 0
			copied = copy.copy(next_section)
			if next_section != '' and next_section != ' ' and next_section != ')':
				next_sections.append(copied)
			next_section = ''

		if start_count == stop_count and start_count > 0:
			break

		if start_count >= 2:
			next_section += letter



	# Create current node
	node_type, prob, word = parse_node(tree)
	current_node = StanfordNode(parent=parent, node_type=node_type, probability=prob, word=word)
	if parent != None:
		kids = copy.copy(current_node.parent.children)
		kids.append(current_node)
		current_node.parent.children = kids
	if root_node == None:
		root_node = current_node



	#Create children
	for section in next_sections:
		count += 1
		parse(section, current_node, root_node, count)
	return root_node

def parse_node(node):
	node_type = re.search("\A\s?\((\w*)", node).group(1)
 	prob = re.search("\A\s?\(\w* \[(\d{0,2}\.\d*)\]", node)
	word = re.search("\A\s?\(\w* \[(\d{0,2}\.\d*)\] (\w*)", node)
	if word != None:
		word = word.group(2)
	if prob != None:
		prob = prob.group(1)
	return node_type, prob, word
