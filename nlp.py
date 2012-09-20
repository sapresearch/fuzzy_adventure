import re
import nltk
from nltk.stem import PorterStemmer

def tokens(string):
	words = nltk.word_tokenize(string)
	tokenized = []
	for w in words:
		tokenized += w.split("_")
	
	un_cameled = []
	camel = re.compile("(.*)(Date|Name|Place)") # hard-coded for DBpedia
	for t in tokenized:
		out = camel.match(t)
		if out == None:
			un_cameled.append(t)
		else:
			un_cameled.append(out.group(1))
			un_cameled.append(out.group(2))

	stemmed = []
	for u in un_cameled:
		s = PorterStemmer().stem(u)
		stemmed.append(s.lower())

	filtered = filter(lambda s: s != '?' and s != ',' and s != '.' and s != "'s", stemmed)
	return filtered

def remove_stopwords(words):
	no_stopwords = [w.strip() for w in words if w.strip() not in nltk.corpus.stopwords.words('english')]
	return no_stopwords

def lexical_type(triplet):
	lex_type = 'unknown'
	title = triplet[title]
	types = {'name': ['name', 'surname', 'givenName'], 'date': ['birthDate', 'deathDate'], 'location': ['birthPlace', 'deathPlace'], 'occupation': ['description']}
	for type_name, titles in types.items():
		if title in titles:
			lex_type = type_name
	return lex_type
