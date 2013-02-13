import sys
import string
from  semanticNet import *
from answerGenerator import *
from keyWords import *
from semanticNet import *
import wordnet_synonym 
from glossary import *
import en

def nlp_nlidb(question):

	allWords = ''
	main_q=[]
	'''STEP1: Extracting the keywords using keyWordExtraction:'''
	Nouns, Verbs, adjs_prpos, question_type = formatKeyWords(question)
	r = ''
	print 'question_type = ', question_type
	#remove the auxiliary verb 'to be':
	for v in Verbs:
		if en.verb.infinitive(v) == 'be':
			r = v
	print '*'*30
	'''combine all key words extracted for each category:'''
	keyWords = list(Nouns+ Verbs+ adjs_prpos)
	'''remove empty elements:'''
	while '' in keyWords:
		keyWords.remove('')
	# print 'keyWords: ', keyWords
	'''STEP2: Check the glossary:'''
	glossaryMatches, remove_list = checkGlossary(question)
	remove_list.append(r)


	conditions = set()
	tables = set()
	defaultValues = set()
	what = set()
	allWords = list(set(keyWords + glossaryMatches))


	allWords, conditions, what = answerGenerator(question, allWords, conditions, what)

	keyWords = [x for x in keyWords if x not in remove_list]
	allWords = list(set(keyWords + glossaryMatches))

	foundTables, def_vals = createRelations(allWords, what, tables)
	# tables.update(foundTables)
	tables.update(foundTables)
	defaultValues.update(def_vals)

	return allWords, defaultValues, what, conditions, tables, question_type
 
# print output

