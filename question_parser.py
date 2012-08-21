import nltk

data = [ ['live', 'tigers', 'india'], ['born', 'einstein', 'germany'] ]

def pos_tag(sentence):
	tree = nltk.pos_tag(nltk.word_tokenize(sentence.lower()))
	return tree

def triples(tree):
	noun_tags = ['NN', 'NNS', 'NNP', 'NNPS']
	verb_tags = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
	subj = ''
	obj = ''
	verb = ''
	for t in tree:
		if t[1] in noun_tags:
			if subj == '':
				subj = t[0]
			elif obj == '':
				obj = t[0]
		elif t[1] in verb_tags:
			if verb == '' and subj != '':
				verb = t[0]
	return subj, obj, verb

def answer(terms):
	ans = "I don't know"
	for triple in data:
		in_triple = 0
		for term in terms:
			if term in triple:
				in_triple += 1
		if in_triple >= 2:
			ans = triple
	return ans

def question(sentence):
	return answer(triples(pos_tag(sentence)))

query = raw_input("Enter a question to parse\n")
print question(query)
