import sys
sys.path.append('../external/stanford-parser-2008-10-26/stanford-parser.jar')
sys.path.append('../external/ogrisel-dbpediakit-400677b')
from java.io import CharArrayReader
from edu.stanford.nlp import *
from SimpleXMLRPCServer import SimpleXMLRPCServer


def tree(sentence):
	lp = parser.lexparser.LexicalizedParser('../external/stanford-parser-2008-10-26/englishPCFG.ser.gz')
	lp.setOptionFlags(["-maxLength", "80", "-retainTmpSubcategories"])

	tlp = trees.PennTreebankLanguagePack()
	toke = tlp.getTokenizerFactory().getTokenizer(CharArrayReader(sentence));
	wordlist = toke.tokenize()
		 
	if (lp.parse(wordlist)):
		parse = lp.getBestParse()
			 
	gsf = tlp.grammaticalStructureFactory()
	gs = gsf.newGrammaticalStructure(parse)
	dependencies = gs.typedDependenciesCollapsed()

	parse = parse.toString()
	return parse#, dependencies


server = SimpleXMLRPCServer(('localhost', 9001), logRequests=True)
server.register_function(tree)
server.serve_forever()