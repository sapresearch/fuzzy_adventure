import sys
sys.path.append("/home/I829287/fuzzy_adventure/query_decomposition")
sys.path.append("/home/I829287/fuzzy_adventure/search")
import penn_treebank_node
import triplet_extraction
import question_type
import stanford_client
import ensemble
import nlp



""" Main application function. """
def ask_question(question):
	triplet, synonyms, lexical_type, tree = question_decomposition(question)
	answer, confidence, full_answers = answer_search(synonyms, lexical_type)
	return answer, confidence, lexical_type, full_answers, tree, triplet, synonyms

def question_decomposition(question):
	lexical_type = question_type.classify(question)

	tree = stanford_client.to_tree(question)
	root = penn_treebank_node.parse(tree)
	nodes, _ = triplet_extraction.question_analysis(root)

	""" Create an array with each word and it's synonyms in a subarray:
	["Albert", "born"] becomes [["albert"], ["einstein"], ["born", "birth", "birthplace"]] """
	synonyms = []
	for n in nodes:
		for word in n.chunk():
			syns = word.synonyms()
			string = " ".join(syns)
			tokens_list = nlp.tokens(string)
			synonyms.append(tokens_list)
	
	return nodes, synonyms, lexical_type, tree

def answer_search(triplet, lexical_type):
	if len(triplet) <= 1:
		answer = "I don't understand the question"
		confidence, full_answers, synonyms = 0., [], []
	else:
		answer, confidence, full_answers = ensemble.search(triplet, lexical_type)
	return answer, confidence, full_answers
