import dbpedia_parser as dp
import stanford_parser as stanford_parser
import stanford_client
import triplet_extraction
import time


#dp.search('Bennelong', 'died') #third parameter is optional
#dp.search('Tol_Avery', 'Avery', 'surname') #only returns true or false (we are returning the data row for now

# Main application function
def ask_question(question):
	tree = stanford_client.to_tree(q)
	root = stanford_parser.parse(tree)
	top_node = root.children[0]
	query, question_type = triplet_extraction.question_analysis(top_node)
	return query, question_type

q = "Where do tigers live?"
q = "When was Albert Einstein born?"
q = "Where is the North Pole located?"
q = "Where is the best French restaurant in San Francisco?"

start = time.time()
print ask_question(q)

duration = time.time() - start
print "Time: " + str(duration)
