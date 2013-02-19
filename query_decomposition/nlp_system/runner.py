from nlp_nlidb import *
import os

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
		'''print question'''
		allWords, defaultValues, what, conditions, tables, question_type = nlp_nlidb(question)

		print 'allWords: ', allWords
		print_defaultValue = 'Default value: NOT FOUND'
		print_condition = 'Condition: NOT FOUND'
		print_table = 'Table: NOT FOUND'
		print_table = 'Tables: '+ str(list(tables))
		if defaultValues!=[]:
				print_defaultValue = 'Default value: ' + str(list(defaultValues))
		print_condition = 'Conditions: ' + str(list(conditions))

		print print_table
		print print_defaultValue
		print print_condition
