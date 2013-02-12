import sys
import string
from  semanticNet import *
from answerGenerator import *
from semanticNet import *
import wordnet_synonym 
from createGlossary import createGlossary
import keyWordsExtraction
from stanford_client import to_tree
import penn_treebank_node
import en
import os
# from nltk import WordNetLemmatizer as WN_Lemmatizer
# from nltk.stem import PorterStemmer as PStemmer


sys.path.append("/home/I837185/git/fuzzy_adventure/query_decomposition")
sys.path.append("/home/I837185/stemming-1.0/stemming")



# sys.path.append("/home/I837185/git/fuzzy_adventure/query_decomposition/nlp_system")
# import triplet_extraction


def extractKeyWords(question):
	buf=[]
	nouns = []
	verbs = []
	adjs_prpos = []
	tree = to_tree(question)
	keyWords_allNull = 0
	print tree
	root = penn_treebank_node.parse(tree)
	keyWords, question_type = keyWordsExtraction.keyWordsExtraction(root)
	# print question_type
	possesive_adjs = ['my','your','his','her','their','its','our']
	# check for all three keys of the dictionary if they are empty:
	if ([a for a in keyWords.values() if a == []]):
		keyWords_allNull = keyWords_allNull  + 1
	if keyWords_allNull==3:
                print("No keywords found! \r\n")
        else:
            # temp = []
            for n in keyWords['Nouns']:
            	if n!= None:
            		# n_lemmatized = WN_Lemmatizer().lemmatize(n.word)
            		# nouns.append(str(n_lemmatized))
            		nouns.append(str(n.word))
            for v in keyWords['Verbs']:
            	if v!= None:
            		# v_stemmed = PStemmer().stem(v.word)
            		# verbs.append(str(v_stemmed))
            		verbs.append(str(v.word))

            for adj in keyWords['Adjectives and Propositions']:
            	if adj!= None:
            		adjs_prpos.append(str(adj.word))

            # print temp
            q_noPunc = question.translate(string.maketrans("",""), string.punctuation)
            words = q_noPunc.split()
            for w in words:
            	if w in possesive_adjs:
            		adjs_prpos.append(w)

 	return nouns,verbs, adjs_prpos, question_type




def checkGlossary(question):
	#check the words
	glossaryMatches = []
	remove_list = []
	q_noPunc = question.translate(string.maketrans("",""), string.punctuation)
	words = q_noPunc.split(" ")
	for w in words:
		w = w.lower()
		if en.is_noun(w):
			w = en.noun.singular(w)
		elif en.is_verb(w):
			w = en.verb.infinitive(w)

	glossary_one_word, glossary_two_words, glossary_three_words, glossary_four_words = createGlossary()
	#check four words glossary:
	phrase = ''
	for i in range(len(words)-3):
		phrase = ' '. join(words[i:i+4])
		if phrase in glossary_four_words:
			glossaryMatches.append(glossary_four_words[phrase])
			for w in words[i:i+4]:
				remove_list.append(w)
			words = [x for x in words if x not in phrase.split()]

	#check three words glossary:
	phrase = ''
	for i in range(len(words)-2):
		phrase = ' '. join(words[i:i+3])
		if phrase in glossary_three_words:
			glossaryMatches.append(glossary_three_words[phrase])
			for w in words[i:i+3]:
				remove_list.append(w)
			words = [x for x in words if x not in phrase.split()]
	#check two words glossary:
	phrase = ''
	for i in range(len(words)-1):
		phrase = ' '. join(words[i:i+2])
		if phrase in glossary_two_words:
			glossaryMatches.append(glossary_two_words[phrase])
			for w in words[i:i+2]:
				remove_list.append(w)
			words = [x for x in words if x not in phrase.split()]

	#check one word glossary:
	for k in question.split() :
		if k.strip() in glossary_one_word:
			glossaryMatches.append(glossary_one_word[k])
			remove_list.append(k)

	# print 'glossaryMatches = ', glossaryMatches
	# print remove_list
	return glossaryMatches, remove_list



def clear():
    if os.name == 'posix':
        os.system('clear')

    elif os.name == ('ce', 'nt', 'dos'):
        os.system('cls')

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
clear()
print '*'*80
print '*'*80
print '*',' '*10, 'WELCOME TO THE FUZZY ADVENTURE\'S QUESTION_ANSWER SYSTEM', ' '*9,'*'
print '*'*80
print '*'*80
print "Enter the question. To exit press enter: "
while True:
	print '=' * 80
	question = raw_input('>> ')
	if question =='':
		break
	else: 
		allWords = ''
		main_q=[]
		'''STEP1: Extracting the keywords using keyWordExtraction:'''
		Nouns, Verbs, adjs_prpos, question_type = extractKeyWords(question)
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

		glossaryMatches, remove_list = checkGlossary(question)
		remove_list.append(r)

		"""check if any condition is in the allWords:"""
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
		defaultValues. update(def_vals)

		''' Output '''

		print 'allWords: ', allWords
		# print_what = 'Look for: UNKOWN'
		print_defaultValue = 'Default value: NOT FOUND'
		print_condition = 'Condition: NOT FOUND'
		print_table = 'Table: NOT FOUND'

		what.add(question_type)
		for w in what:	
			table = findTable(w)
			if table != '':
				tables.add(table)
				defaultValues.add(checkDB(w, table))


				
		# print_what = 'Look for: ' + str(list(what))
		print_table = 'Tables: '+ str(list(tables))
		if defaultValues!=[]:
				print_defaultValue = 'Default value: ' + str(list(defaultValues))
		print_condition = 'Conditions: ' + str(list(conditions))

		# print print_what
		print print_table
		print print_defaultValue
		print print_condition

		# print output




















