
from nlp_nlidb import *
import os
from components import *

def clear():
    if os.name == 'posix':
        os.system('clear')

    elif os.name == ('ce', 'nt', 'dos'):
        os.system('cls')

from fuzzy_adventure.hana import connection

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
        allWords, defaultValues, what, conditions, all_tables, question_type, Proper_Nouns = nlp_nlidb(question)

        print 'allWords: ', allWords
        print "table:",all_tables
        '''required_values is not being used in our system anymore'''
        # print "default Values:", defaultValues
        print "conditions: ",conditions
        print "question_type:", question_type
        print "what: ", what
        print "Proper Nouns: ", Proper_Nouns
        test = components.get_components()


        # print_defaultValue = 'Default value: NOT FOUND'
        # print_condition = 'Condition: NOT FOUND'
        # print_table = 'Table: NOT FOUND'
        
        # # all_tables = []
        # # what.add(question_type)
        # # for w in what:    
        # #     # print '1', what
        # #     table = semanticNet.tables(w)
        # #     # print 'table:', table
        # #     all_tables.append(table)
        # #     # print 'all', all_tables
        # #     defaultValues.append(semanticNet.required_values(w, table))
        # if defaultValues!=[]:
        #     print_defaultValue = 'Default value: ' + str(list(defaultValues))
        #     print_condition = 'Conditions: ' + str(list(conditions))
        # if all_tables !=[]:
        #     print_table = 'Tables: '+ str(list(all_tables))

        # print print_table
        # print print_defaultValue
        # print print_condition
