import wordnet_synonym
import sys
sys.path.append("../")
import nlp

def synonyms(word):
	synonyms = wordnet_synonym.synonyms(word)
	no_stopwords = nlp.remove_stopwords(synonyms)
	return no_stopwords
