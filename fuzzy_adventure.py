import sys
sys.path.append("/home/I829287/fuzzy_adventure/models")
sys.path.append("/home/I829287/fuzzy_adventure/query_decomposition")
import penn_treebank_parser as penn_treebank_parser
import triplet_extraction
import question_type
import stanford_client
import ensemble
import re



""" Main application function. """
def ask_question(question):
	triplet, lexical_type, tree = question_decomposition(question)
	answer, confidence, full_answers, synonyms = answer_search(triplet, lexical_type)
	return answer, confidence, lexical_type, full_answers, tree, triplet, synonyms

def question_decomposition(question):
	lexical_type = question_type.classify(question)

	tree = stanford_client.to_tree(question)
	root = penn_treebank_parser.parse(tree)
	nodes, _ = triplet_extraction.question_analysis(root)
	triplet = []
	for n in nodes:
		if n != '?' and type(n) != bool:
			triplet.append(n)
	return triplet, lexical_type, tree

def answer_search(triplet, lexical_type):
	if len(triplet) <= 1:
		answer = "I don't understand the question"
		confidence, full_answers, synonyms = 0., [], []
	else:
		answer, confidence, full_answers, synonyms = ensemble.search(triplet, lexical_type)
	return answer, confidence, full_answers, synonyms

""" This is here because if it's in the question_test.py file, then there's a loop when
question_test requires fuzzy_adventure, which requires question_type, which requires question_test """
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
