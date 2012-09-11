import stanford_parser as sp

noun_labels = ['NN', 'NNP', 'NNPS', 'NNS']
verb_labels = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
adjective_labels = ['JJ', 'JJR', 'JJS']

# Implemented from "Triplet Extraction from Sentences"
def extract_triplet(tree):
	np_subtree = tree.descendent(["NP"])
	vp_subtree = tree.descendent(["VP"])

	subject = extract_subject(np_subtree)
	predicate = extract_predicate(vp_subtree)
	obj = extract_object(predicate)
	triplet = [subject, predicate, obj]
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
    obj = False
    for sibling in siblings:
        if sibling.node_type in predicate_siblings:
            result.append(sibling)
    for r in result:
        if obj == False:
            if (r.node_type == 'NP' or r.node_type == 'PP'):
                obj = r.descendent(noun_labels)
            elif r.node_type == 'ADJP':
                obj = r.descendent(adjective_labels)
    return obj
	
# Implemented from "Question Answering Based on Semantic Graphs"
def question_analysis(top_node):
	question_type = 'unknown'
	query = False

	n0 = top_node.children[0]
	n1 = top_node.node_index(1)
	n2 = top_node.node_index(2)
	n3 = top_node.node_index(3)
	n4 = top_node.node_index(4)
	n5 = top_node.node_index(5)

	if top_node.node_type == 'SQ':
		if n1.node_type == 'NP':
			question_type = 'yes_no'
			subject = extract_object(n1)
			if n2.node_type == 'NP':
				predicate = extract_predicate(n0)
				obj = extract_subject(n2)
				query = [subject, predicate, obj]
			else:
				predicate = extract_predicate(n2)
				obj = extract_object(predicate)
				query = [subject, predicate, obj]
	elif top_node.node_type == 'SBARQ':
		if n0.node_type == 'WHNP' and n1.node_type == 'SQ':
			question_type = 'list'
			if n3.node_type == 'VP':
				predicate = extract_predicate(n3)
				obj = extract_object(predicate)
				query = ['?', predicate, obj]
			elif n4.node_type == 'NP' and n5.node_type == 'VP':
				subject = extract_subject(n4)
				predicate = extract_predicate(n5)
				query = [subject, predicate, '?']
		elif n0.node_type == 'WHADVP' and n1.node_type == 'SQ' and n4.node_type == 'NP':
			# We skipped the "why" part of the algorithm.
			# We skipped the reasonFilter part.
			if n5.node_type == 'VP':
				has_where = top_node.word_search('where')
				has_when = top_node.word_search('when')
				subject = extract_subject(n4)
				predicate = extract_predicate(n5)
				if has_where != False:
					question_type = "location"
					query = [subject, predicate, '?']
				elif has_when != False:
					question_type = "time"
					query = [subject, predicate, '?']
				# skipped the reasonFilter else loop.
		elif n0.node_type in ['WHADJP', 'WHNP'] and n1 in ['S', 'SQ']:
			question_type = 'quantity'
			if n3.node_type == 'VP':
				predicate = extract_predicate(n3)
				query = ['?', predicate, '?']
			elif n3.node_type == 'NP' and n4.node_type == 'VP':
				predicate = extract_predicate(n4)
				query = ['?', predicate, '?']
	return query, question_type
