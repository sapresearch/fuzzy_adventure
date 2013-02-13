import sys
from nlp_nlidb import *
import keyWords
# import string
# from  semanticNet import *
# from answerGenerator import *
# from keyWords import *
# from semanticNet import *
# import wordnet_synonym 
# from glossary import *
# import en
import os
# from nltk import WordNetLemmatizer as WN_Lemmatizer
# from nltk.stem import PorterStemmer as PStemmer


sys.path.append("/home/I837185/git/fuzzy_adventure/query_decomposition")
sys.path.append("/home/I837185/stemming-1.0/stemming")


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
		# print question
		allWords, defaultValues, what, conditions, tables, question_type = nlp_nlidb(question)

		print 'allWords: ', allWords
		# print_what = 'Look for: UNKOWN'
		print_defaultValue = 'Default value: NOT FOUND'
		print_condition = 'Condition: NOT FOUND'
		print_table = 'Table: NOT FOUND'

		what.add(question_type)
		'''!!!!!!check'''
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



















