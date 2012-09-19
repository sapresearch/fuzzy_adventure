from nltk.corpus import wordnet
import re

def synonyms(word):
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
