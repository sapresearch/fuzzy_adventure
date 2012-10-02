import penn_treebank_parser as penn_treebank_parser
import triplet_extraction
import time
import sys
sys.path.append("/home/I829287/fuzzy_adventure/search_clients")
sys.path.append("/home/I829287/fuzzy_adventure/models")
import question_type
import stanford_client
import ensemble
import re



""" Main application function. """
def ask_question(question):
	start = time.time()
	tree = stanford_client.to_tree(question)
	root = penn_treebank_parser.parse(tree)
	top_node = root.children[0]
	nodes, _ = triplet_extraction.question_analysis(top_node)
	lexical_type = question_type.classify(question)
	parse_time = time.time() - start
	triplet = []
	for n in nodes:
		if n != '?' and type(n) != bool:
			triplet.append(n)
	if len(triplet) <= 1:
		answer = "I don't understand the question"
		confidence, full_answers, synonyms, search_time = 0., [], [], 0.
	else:
		start = time.time()
		answer, confidence, full_answers, synonyms = ensemble.search(triplet, lexical_type)
		search_time = time.time() - start
	return answer, confidence, lexical_type, full_answers, tree, triplet, synonyms, parse_time, search_time

def load_data(file_name):
	questions, answers, lex_types = [], [], []
	f = file(file_name)
	for line in f.readlines():
		line = line.split("\t")
		lex_type = line.pop(-1)
		lex_type = re.sub("[\r\n]", '', lex_type)
		question = line.pop(0)
		answer = line

		lex_types.append(lex_type)
		questions.append(question)
		answers.append(answer)
	return questions, answers, lex_types
