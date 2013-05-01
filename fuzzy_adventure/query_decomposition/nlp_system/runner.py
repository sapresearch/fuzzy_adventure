<<<<<<< HEAD
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
        allWords, defaultValues, what, conditions, all_tables, question_type = nlp_nlidb(question)

        print 'allWords: ', allWords
        print "table:",all_tables
        '''required_values is not being used in our system anymore'''
        # print "default Values:", defaultValues
        print "conditions: ",conditions
        print "question_type:", question_type
        print "what: ", what
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
# ======================================================================================

#     print 'allWords: ', allWords
# # print_what = 'Look for: UNKOWN'
# print_defaultValue = 'Default value: NOT FOUND'
# print_condition = 'Condition: NOT FOUND'
# print_table = 'Table: NOT FOUND'

# what.add(question_type)
# for w in what:    
# table = findTable(w)
# if table != '':
# tables.add(table)
# defaultValues.add(checkDB(w, table))



# # print_what = 'Look for: ' + str(list(what))
# print_table = 'Tables: '+ str(list(tables))
# if defaultValues!=[]:
# print_defaultValue = 'Default value: ' + str(list(defaultValues))
# print_condition = 'Conditions: ' + str(list(conditions))

# # print print_what
# print print_table
# print print_defaultValue
# print print_condition

=======
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
        allWords, defaultValues, what, conditions, all_tables, question_type = nlp_nlidb(question)

        print 'allWords: ', allWords
        print_defaultValue = 'Default value: NOT FOUND'
        print_condition = 'Condition: NOT FOUND'
        print_table = 'Table: NOT FOUND'
        
        # all_tables = []
        # what.add(question_type)
        # for w in what:    
        #     # print '1', what
        #     table = semanticNet.tables(w)
        #     # print 'table:', table
        #     all_tables.append(table)
        #     # print 'all', all_tables
        #     defaultValues.append(semanticNet.required_values(w, table))
        if defaultValues!=[]:
            print_defaultValue = 'Default value: ' + str(list(defaultValues))
            print_condition = 'Conditions: ' + str(list(conditions))
        if all_tables !=[]:
            print_table = 'Tables: '+ str(list(all_tables))

        print print_table
        print print_defaultValue
        print print_condition
# ======================================================================================

#     print 'allWords: ', allWords
# # print_what = 'Look for: UNKOWN'
# print_defaultValue = 'Default value: NOT FOUND'
# print_condition = 'Condition: NOT FOUND'
# print_table = 'Table: NOT FOUND'

# what.add(question_type)
# for w in what:    
# table = findTable(w)
# if table != '':
# tables.add(table)
# defaultValues.add(checkDB(w, table))



# # print_what = 'Look for: ' + str(list(what))
# print_table = 'Tables: '+ str(list(tables))
# if defaultValues!=[]:
# print_defaultValue = 'Default value: ' + str(list(defaultValues))
# print_condition = 'Conditions: ' + str(list(conditions))

# # print print_what
# print print_table
# print print_defaultValue
# print print_condition

>>>>>>> 1fb6ded45ada99e511032183b2346e8fa99840f5
