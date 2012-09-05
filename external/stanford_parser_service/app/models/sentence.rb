require 'java'
include Java
require "~/fuzzy_adventure/external/stanford-parser-2008-10-26/stanford-parser.jar"
#require "~/fuzzy_adventure/external/stanford-parser-2011-09-14/stanford-parser.jar"
include_class 'java.io.StringReader'
include_class 'edu.stanford.nlp.parser.lexparser.LexicalizedParser'
include_class 'edu.stanford.nlp.trees.PennTreebankLanguagePack'

class Sentence < ActiveRecord::Base
	self.abstract_class = true

	PARSER = LexicalizedParser.new("/home/I829287/fuzzy_adventure/external/stanford-parser-2008-10-26/englishPCFG.ser.gz")
	PTLP = PennTreebankLanguagePack.new

	def self.parse(sentence)
		toke = PTLP.getTokenizerFactory().getTokenizer(StringReader.new(sentence))
		wordlist = toke.tokenize()
		PARSER.parse(wordlist) ? PARSER.getBestParse() : nil
	end


	def self.stanford_tree(sentence)
		#PARSER.setOptionFlags(["-maxLength", "80", "-retainTmpSubcategories"]) 

		toke = PTLP.getTokenizerFactory().getTokenizer(StringReader.new(sentence))
		wordlist = toke.tokenize()
		 
		if PARSER.parse(wordlist)
			parse = PARSER.getBestParse()
		end
			 
		gsf = PTLP.grammaticalStructureFactory()
		gs = gsf.newGrammaticalStructure(parse)
		dependencies = gs.typedDependenciesCollapsed()
			  
		return parse, dependencies.toString()
	end

end
