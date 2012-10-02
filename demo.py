import fuzzy_adventure
import re
import time

def demo(verbose=False):
	while True:
		print "Ask a question:"
		question = raw_input()

		verbose = re.match(".*-v", question) != None
		question = re.sub("-v", '', question)

		start = time.time()
		answer, confidence, lexical_type, all_answers, tree, triplet, synonyms, parse_time, search_time = fuzzy_adventure.ask_question(question)
		duration = time.time() - start

		if verbose:
			print "Time: " + str(round(duration, 3))
			print "  Parse time: " + str(round(parse_time, 3))
			print "  Search time: " + str(round(search_time, 3))
			print "Parse Stack:"
			print " Lexical Answer Type: " + lexical_type
			print "  Tree: " + str(tree)
			triplet_words = []
			for t in triplet:
				triplet_words.append(t.word)
			print "  Parsed triplet: " + str(triplet_words)
			print "  Synonyms: " + str(synonyms)
			print "  All answers: " + str(all_answers)
			print "Confidence: " + str(confidence)
			
		print "Answer: " + answer + "\n"
	return None

demo()
