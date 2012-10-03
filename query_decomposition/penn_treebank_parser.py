import copy
import re
import sys
sys.path.append("/home/I829287/fuzzy_adventure/search")
import synonym

class PennTreebankNode():
    def __init__(self, node_type='ROOT', word=None, probability=0.0, children=[], parent=None, index=None):
        self.node_type = node_type
        self.word = word
        self.probability = probability
        self.children = children
        self.parent = parent
        self.index = index

    """ Return a list of proper nouns, if a node is a proper noun """
    def chunk(self):
        output = [self]
        if self.node_type == 'NNP' or self.node_type == 'NNPS':
            for s in self.siblings():
                if s.index == self.index+1:
                    output.append(s)
        return output

    def synonyms(self):
        if self.node_type != 'NNP' and self.node_type != 'NNPS':
            output = synonym.synonyms(self)
        else:
            output = [self.word]
        return output

    def descendent(self, node_types, bfs = True):#true = breadth first search (bfs); depth first search (dfs) otherwise
        kids = copy.copy(self.children)
        if bfs == False:#for deepest node
            last = None
            for k in kids:
                if k.node_type in node_types:
                    last = k
                kids += k.children
            return last
        else:#for breadth first search
            for k in kids:
                if k.node_type in node_types:
                    return k
                else:
                    kids += k.children
            return False

    def node_index(self, i):
        kids = copy.copy(self.children)
        for k in kids:
            if k.index == i:
                return k
            else:
                kids += k.children
        return False

    def word_search(self, word):
        kids = copy.copy(self.children)
        for k in kids:
            if k.word.lower() == word.lower():
                return k
            else:
                kids += k.children
        return False

    def siblings(self):
        parent = self.parent
        kids = copy.copy(parent.children)
        kids.remove(self)
        return kids


def parse(tree, parent=None, root_node=None, count=0, debug=False):
	tree = re.sub('(\(ROOT )(.*)(\))', '\\2', tree)
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
	current_node = PennTreebankNode(parent=parent, node_type=node_type, probability=prob, word=word)
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
	
	root_node.index = 'TN'
	kids = copy.copy(root_node.children)
	count = 0
	for child in kids:
		if child.word != '.' and child.word != '?':
			child.index = count
			count += 1
			kids += child.children

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
