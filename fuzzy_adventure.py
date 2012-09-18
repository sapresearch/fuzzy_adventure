import dbpedia_parser as dp
import stanford_parser as stanford_parser
import stanford_client
import triplet_extraction
import time
import mongo_api
import sys
sys.path.append("./search_clients")
import triplet_search
import re



""" Main application function. """
def ask_question(question):
	start = time.time()
	tree = stanford_client.to_tree(question)
	root = stanford_parser.parse(tree)
	top_node = root.children[0]
	nodes, question_type = triplet_extraction.question_analysis(top_node)
	parse_time = time.time() - start
	triplet = []
	for n in nodes:
		if n != '?' and type(n) != bool:
			triplet.append(n.word.lower())
	if len(triplet) == 0:
		answer = "I don't understand the question"
		search_time = 0.
	else:
		triplet = [ [triplet[0]], [triplet[1]] ]
		start = time.time()
		answer = triplet_search.search(triplet)
		search_time = time.time() - start
		if len(answer) == 0:
			answer = "I don't know"
		else:
			answer = answer[0]
	return answer, triplet, tree, parse_time, search_time

def demo(verbose=False):
	while True:
		print "Ask a question:"
		question = raw_input()

		start = time.time()
		answer, triplet, tree, parse_time, search_time = ask_question(question)
		duration = time.time() - start

		verbose = re.match(".*-v", question) != None
		if verbose:
			print "Time: " + str(round(duration, 3))
			print "Parse time: " + str(round(parse_time, 3))
			print "Search time: " + str(round(search_time, 3))
			print "Tree: " + str(tree)
			print "Parsed triplet: " + str(triplet)
			
		print "Answer: " + answer + "\n"
	return None
