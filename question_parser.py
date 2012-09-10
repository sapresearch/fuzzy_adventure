import sys
sys.path.append('./external/stanford-parser-2008-10-26/stanford-parser.jar')
sys.path.append('./external/ogrisel-dbpediakit-400677b')
from java.io import CharArrayReader
from edu.stanford.nlp import *
import re

# For testing only
data = [ ['live', 'tigers', 'india'], ['born', 'einstein', 'germany'] ]

def stanford_tree(sentence):
	lp = parser.lexparser.LexicalizedParser('./external/stanford-parser-2008-10-26/englishPCFG.ser.gz')
	lp.setOptionFlags(["-maxLength", "80", "-retainTmpSubcategories"])

	tlp = trees.PennTreebankLanguagePack()
	toke = tlp.getTokenizerFactory().getTokenizer(CharArrayReader(sentence));
	wordlist = toke.tokenize()
		 
	if (lp.parse(wordlist)):
		parse = lp.getBestParse()
			 
	gsf = tlp.grammaticalStructureFactory()
	gs = gsf.newGrammaticalStructure(parse)
	dependencies = gs.typedDependenciesCollapsed()
			  
	return parse.toString(), dependencies

# return the subject, predicate and object of the question.
def triple(sentence):
	obj_relations = ['dobj', 'prep_in', 'prep_to']
	subj, pred, obj = '', '', ''
	for rel in sentence:
		relation_type = rel.reln().toString()
		if relation_type == 'nsubj':
			pred, subj = rel.gov(), rel.dep()
		elif relation_type in obj_relations:
			obj = rel.dep()
	return subj, pred, obj

def subject(sentence):
	np_subtree = re.search('\(NP.*', tree)
	subj = re.search('\((NN|NNP|NNPS|NNS) \[[\d.]*\] ([^\)]*)', np_subtree.group(0))
	return subj.group(2)

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


string = 'A rare black squirrel has become a regular visitor to a suburban garden.'
print stanford_tree(string)