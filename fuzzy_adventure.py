import penn_treebank_parser as penn_treebank_parser
import triplet_extraction
import time
import mongo_api
import re
import sys
sys.path.append("/home/I829287/fuzzy_adventure/search_clients")
import triplet_search
import stanford_client



""" Main application function. """
def ask_question(question):
	start = time.time()
	tree = stanford_client.to_tree(question)
	root = penn_treebank_parser.parse(tree)
	top_node = root.children[0]
	nodes, question_type = triplet_extraction.question_analysis(top_node)
	parse_time = time.time() - start
	triplet = []
	for n in nodes:
		if n != '?' and type(n) != bool:
			triplet.append(n.word.lower())
	if len(triplet) == 0:
		answer = "I don't understand the question"
		full_answers = []
		synonyms = []
		search_time = 0.
	else:
		triplet = [ [triplet[0]], [triplet[1]] ]
		start = time.time()
		answers, full_answers, synonyms = triplet_search.search(triplet)
		search_time = time.time() - start
		if len(answers) == 0:
			answer = "I don't know"
		else:
			answer = answers[0]
	return answer, full_answers, tree, triplet, synonyms, parse_time, search_time

def demo(verbose=False):
	while True:
		print "Ask a question:"
		question = raw_input()

		verbose = re.match(".*-v", question) != None
		question = re.sub("-v", '', question)

		start = time.time()
		answer, all_answers, tree, triplet, synonyms, parse_time, search_time = ask_question(question)
		duration = time.time() - start

		if verbose:
			print "Time: " + str(round(duration, 3))
			print "  Parse time: " + str(round(parse_time, 3))
			print "  Search time: " + str(round(search_time, 3))
			print "Parse Stack:"
			print "  Tree: " + str(tree)
			print "  Parsed triplet: " + str(triplet)
			print "  Synonyms: " + str(synonyms)
			print "  All answers: " + str(all_answers)
			
		print "Answer: " + answer + "\n"
	return None

#demo()
