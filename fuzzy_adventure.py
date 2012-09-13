import dbpedia_parser as dp
import stanford_parser as stanford_parser
import stanford_client
import triplet_extraction
import time
import mongo_api



""" Main application function. """
def ask_question(question):
	tree = stanford_client.to_tree(q)
	root = stanford_parser.parse(tree)
	top_node = root.children[0]
	nodes, question_type = triplet_extraction.question_analysis(top_node)
	triplet = []
	for n in nodes:
		if n != '?':
			triplet.append(n.word.lower())
	answer = mongo_api.find_by_words(triplet)
	return answer, triplet



q = "Where is the North Pole located?"
q = "When did Albert Einstein die?"
q = "Where do tigers live?"
q = "When was Albert Einstein born?"
q = "Where is the best French restaurant in San Francisco?"

start = time.time()
answer, triplet = ask_question(q)
duration = time.time() - start

print "Time: " + str(duration)
print "Question: " + q
print "Parsed triplet: " + str(triplet)
print "Results: " + str(len(answer))
print "Answer: " + str(answer)
