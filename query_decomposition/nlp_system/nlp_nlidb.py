import sys
import string
from  semanticNet import *
from answerGenerator import answerGenerator
import parser
import semanticNet
import wordnet_synonym 
import glossary
import stanford_client
import penn_treebank_node

def nlp_nlidb(question):

	'''STEP1: Extracting the keywords using Parser:'''
	tree = stanford_client.to_tree(question)
	top_node = penn_treebank_node.parse(tree)
	extracted_words = parser.key_words(top_node, question)
	question_type = parser.questionType(top_node)

	'''STEP2: Replace words with glossary terms:'''
	uniqueWords = glossary.generalizedKeywords(question, extracted_words)
	
	'''STEP3: Adding some manually defined rules'''
	allWords, conditions, target = answerGenerator(question, uniqueWords)

	'''Creating Links between allWords and tables' entities'''
	tables = semanticNet.tables(allWords)
	required_values = semanticNet.required_values(tables, allWords)

	return allWords, required_values, target, conditions, tables, question_type
