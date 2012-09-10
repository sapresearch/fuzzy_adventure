import stanford_parser as sp

noun_labels = ['NN', 'NNP', 'NNPS', 'NNS']
verb_labels = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
adjective_labels = ['JJ', 'JJR', 'JJS']

def extract_triplet(tree):
	np_subtree = tree.descendent(["NP"])
	#print np_subtree.node_type
	vp_subtree = tree.descendent(["VP"])
	#print vp_subtree.node_type

	subject = extract_subject(np_subtree)
	predicate = extract_predicate(vp_subtree)
	object = extract_object(predicate)
	triplet = [subject, predicate, object]
	return triplet


def extract_subject(np_subtree):
	subject = np_subtree.descendent(noun_labels)
	return subject

def extract_predicate(vp_subtree):
    deepest_verb = vp_subtree.descendent(verb_labels, False)
    return deepest_verb

def extract_object(predicate):
    siblings = predicate.siblings()
    predicate_siblings = ['NP', 'PP', 'ADJP']
    result = []
    object = False
    for sibling in siblings:
        if sibling.node_type in predicate_siblings:
            result.append(sibling)
    for r in result:
        if object == False:
            if (r.node_type == 'NP' or r.node_type == 'PP'):
                object = r.descendent(noun_labels)
            elif r.node_type == 'ADJP':
                object = r.descendent(adjective_labels)
    return object






string = '(ROOT (SBARQ [82.494] (WHNP [3.854] (WP [2.692] What)) (SQ [76.704] (VP [76.641] (ADVP [16.203] (RB [15.877] salesperson)) (VBD [4.662] made) (NP [48.802] (NP [13.505] (DT [0.650] the) (JJS [1.444] most) (NNS [4.188] sales)) (PP [34.891] (IN [1.850] in) (NP [32.639] (DT [0.650] the) (NNP [6.213] United) (NNP [9.167] States) (JJ [3.925] last) (NN [5.153] quarter)))))) (. [0.004] ?)))'
string2 = '(ROOT (S [97.578] (NP [38.043] (DT [4.555] A) (JJ [7.773] rare) (JJ [6.278] black) (NN [12.988] squirrel)) (VP [58.394] (VBZ [0.028] has) (VP [54.843] (VBN [5.210] become) (NP [21.991] (DT [1.419] a) (JJ [7.015] regular) (NN [10.787] visitor)) (PP [23.291] (TO [0.003] to) (NP [20.823] (DT [1.419] a) (JJ [8.141] suburban) (NN [8.282] garden))))) (. [0.002] .)))'
root = sp.parse(string)


#np = root.descendent(["NP"])
#print root.descendent(["VP"]).node_type
#print np.descendent(noun_labels).node_type
print extract_triplet(root)[0].word
print extract_triplet(root)[1].word
print extract_triplet(root)[2].word