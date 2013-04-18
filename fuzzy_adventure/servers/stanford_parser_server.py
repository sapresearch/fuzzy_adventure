import sys
import os
project_path = os.environ['FUZZY_ADVENTURE']
sys.path.append(project_path + '/external/stanford-parser-2012-07-09/stanford-parser.jar')
from java.io import CharArrayReader
from edu.stanford.nlp.parser.lexparser import LexicalizedParser
from edu.stanford.nlp import trees
from SimpleXMLRPCServer import SimpleXMLRPCServer

lp = LexicalizedParser.loadModel()

def tree(sentence):
	lp.setOptionFlags(["-maxLength", "80", "-retainTmpSubcategories"])

	tlp = trees.PennTreebankLanguagePack()
	toke = tlp.getTokenizerFactory().getTokenizer(CharArrayReader(sentence));
	wordlist = toke.tokenize()
	parse = lp.apply(wordlist)
			 
	gsf = tlp.grammaticalStructureFactory()
	gs = gsf.newGrammaticalStructure(parse)
	dependencies = gs.typedDependenciesCollapsed()

	parse = parse.toString()
	return parse#, dependencies


def tagged(sentence):
	lp.setOptionFlags(["-maxLength", "80", "-retainTmpSubcategories"])

	tlp = trees.PennTreebankLanguagePack()
	toke = tlp.getTokenizerFactory().getTokenizer(CharArrayReader(sentence));
	wordlist = toke.tokenize()
	parse = lp.apply(wordlist)

	return parse.taggedLabeledYield().toString()


def flatten(sentence):
	lp.setOptionFlags(["-maxLength", "80", "-retainTmpSubcategories"])

	tlp = trees.PennTreebankLanguagePack()
	toke = tlp.getTokenizerFactory().getTokenizer(CharArrayReader(sentence));
	wordlist = toke.tokenize()
	parse = lp.apply(wordlist)

	return parse.flatten().toString()


server = SimpleXMLRPCServer(('localhost', 9001), logRequests=True)
server.register_function(tree)
server.register_function(tagged)
server.register_function(flatten)
server.serve_forever()
