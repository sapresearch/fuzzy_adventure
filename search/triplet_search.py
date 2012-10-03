import xmlrpclib
import sys
sys.path.append("/home/I829287/fuzzy_adventure/query_decomposition")
import nlp

def search(synonyms, lex_type):
	proxy = xmlrpclib.ServerProxy('http://localhost:9000')
	results = proxy.search(synonyms)
	search_words = [item for sublist in synonyms for item in sublist] # flatten it
	selected_fields, full_answers = nlp.extract_field(results, search_words, lex_type)
	return selected_fields, full_answers
