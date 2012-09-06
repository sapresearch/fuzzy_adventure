import stanford_parser as sp

noun_labels = ['NN', 'NNP', 'NNPS', 'NNS']
verb_labels = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
adjective_labels = ['JJ', 'JJR', 'JJS']

def extract_triplet(tree):
	np_subtree = tree.descendent(["NP"])
	print np_subtree.node_type
	vp_subtree = tree.descendent(["VP"])
	print vp_subtree.node_type

	subject = extract_subject(np_subtree)
	predicate = extract_predicate(vp_subtree)
	triplet = [subject]
	return triplet


def extract_subject(np_subtree):
	subject = np_subtree.descendent(noun_labels)
	return subject

def extract_predicate(vp_subtree):
	return None








string = '(ROOT (SBARQ [82.494] (WHNP [3.854] (WP [2.692] What)) (SQ [76.704] (VP [76.641] (ADVP [16.203] (RB [15.877] salesperson)) (VBD [4.662] made) (NP [48.802] (NP [13.505] (DT [0.650] the) (JJS [1.444] most) (NNS [4.188] sales)) (PP [34.891] (IN [1.850] in) (NP [32.639] (DT [0.650] the) (NNP [6.213] United) (NNP [9.167] States) (JJ [3.925] last) (NN [5.153] quarter)))))) (. [0.004] ?)))'
root = sp.parse(string)

#np = root.descendent(["NP"])
#print root.descendent(["VP"]).node_type
#print np.descendent(noun_labels).node_type
print extract_triplet(root)
