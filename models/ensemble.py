import sys
sys.path.append("../search_clients")
import triplet_search

def search(question, lex_type):
	weights = {'triplet_search':1.0}

	answers = triplet_search.search(question, lex_type)
	confidence = {}
	#for a in answers:
		#confidence[a]
	return answers


def vote(answers):
	return None
