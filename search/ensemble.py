import sys
sys.path.append("../search_clients")
import triplet_search

def search(question, lex_type):
	weights = {'triplet_search':1.0}

	selected_fields, full_answers = triplet_search.search(question, lex_type)
	answer, confidence = vote(selected_fields)
	return answer, confidence, full_answers

# TODO 
""" Merge answers from multiple search algorithms """
def vote(answers):
	answer_count = len(answers)
	confidence = 1.0/answer_count if answer_count > 0 else 0.
	if confidence < 0.15:
		answer = "I don't know"
	else:
		answer = answers[0]
	return answer, confidence
