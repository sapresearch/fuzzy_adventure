import dbpedia_parser as dp
import stanford_parser as stanford_parser
import stanford_client
import triplet_extraction
import time
import mongo_api
import re



""" Main application function. """
def ask_question(question):
	tree = stanford_client.to_tree(question)
	root = stanford_parser.parse(tree)
	top_node = root.children[0]
	nodes, question_type = triplet_extraction.question_analysis(top_node)
	triplet = []
	for n in nodes:
		if n != '?':
			triplet.append(n.word.lower())
	if len(triplet) == 0:
		answer = "I don't understand the question"
	else:
		answer = mongo_api.find_by_words(triplet)
		if len(answer) == 0:
			answer = "I don't know"
		else:
			answer = answer[0]
	return answer, triplet

def demo(verbose=False):
	while True:
		print "Ask a question:"
		question = raw_input()

		start = time.time()
		answer, triplet = ask_question(question)
		duration = time.time() - start

		verbose = re.match(".*-v", question) != None
		if verbose:
			print "Time: " + str(duration)
			print "Parsed question: " + str(triplet)
			
		print "Answer: " + answer + "\n"
	return None

demo()
