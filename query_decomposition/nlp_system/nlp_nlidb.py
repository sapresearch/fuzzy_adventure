import sys
import string
from  semanticNet import *
from answerGenerator import answerGenerator
import keyWords
import semanticNet
import wordnet_synonym 
from glossary import *
import en

def nlp_nlidb(question):

	'''STEP1: Extracting the keywords using keyWordExtraction:'''
	nouns, verbs, adjs_prpos, question_type = keyWords.formatKeyWords(question)
	to_remove = []
	"remove the auxiliary verb 'to be':"
	for v in verbs:
		if en.verb.infinitive(v) == 'be':
			 to_remove.append(v)

	'''combine all key words extracted for each category:'''
	extracted_words = nouns + verbs + adjs_prpos
	while '' in extracted_words:
		extracted_words.remove('')

	'''STEP2: Replace words with glossary terms:'''
	glossaryMatches, remove_list = checkGlossary(question)
	unnecessary_words = (remove_list + to_remove)

	extracted_words = [x for x in extracted_words if x not in unnecessary_words]
	uniqueWords = list(set(extracted_words + glossaryMatches))
	allWords, conditions, target = answerGenerator(question, uniqueWords)

	tables, required_values = semanticNet.createRelations(allWords, target)

	return allWords, required_values, target, conditions, tables, question_type
 


question = "Who is the most effective employee on my team?"
question = "Who is the best employee?"
allWords, defaultValues, what, conditions, tables, question_type = nlp_nlidb(question)
#print 'question_type = ', question_type
#print '*'*30
#print allWords
#print defaultValues
