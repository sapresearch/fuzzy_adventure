from nltk.corpus import wordnet
import nlp
import re

def synonyms(word):
	syns = wordnet_synonyms(word)
	no_stopwords = nlp.remove_stopwords(syns)
	return no_stopwords

def wordnet_synonyms(word):
	if is_proper_noun(word):
		return [word]
	word = node_or_string_to_string(word)
	output = [word]
	output += siblings(word)
	output += hyponyms(word)
	output += hypernyms(word)
	return list(set(output))

def siblings(word):
	synsets = wordnet.synsets(word)
	output = _synsets_to_words(synsets)
	return output

def hypernyms(word):
	synsets = wordnet.synsets(word)
	output = []
	for syn in synsets:
		parents = syn.hyponyms()
		output += _synsets_to_words(parents)
	return output

def hyponyms(word):
	synsets = wordnet.synsets(word)
	output = []
	for syn in synsets:
		children = syn.hyponyms()
		output += _synsets_to_words(children)
	return output

def _synsets_to_words(synsets):
	output = []
	for synset in synsets:
		word = synset.name
		word = re.sub("\..*", '', word)
		words = word.split("_")
		output += words
	output = set(output)
	return output

""" Expects input to be an instance of PennTreebankNode """
def is_proper_noun(node):
	if type(node) != str:
		return node.node_type == 'NNP' or node.node_type == 'NNPS'
	else:
		return False # since it's a string and we can't tell it's POS

""" Makes the synonyms function capable of handling both PennTreebankNodes or strings.
Return the node's word if it's a PennTreebankNode, or return the string """
def node_or_string_to_string(word):
	if type(word) != str:
		return word.word
	else:
		return word
