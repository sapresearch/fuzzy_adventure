import en
import string

def checkDB(lookFor, table):
	# print lookFor, table
	# raw_input('')
	defaultValue = ''

	transactions_table = dict()
	components_table =['id','name']
	transactions_table = {'ID' : 'id','TRANSACTION' : 'trans_number','PROGRAMMER' : 'programmer_id','START' : 'start_date','END' : 'end_date','STATUS' :'status','PRIORITY':'priority','CONTRACT PRIORITY' :'contract_priority','PRODUCT' : 'product','COMPONENT ID' :'component_id'}
	programmers_table = ['id','name']

	# find the table, field and default value:
	lookFor = lookFor.lower()
	if (lookFor == 'component'):
		defaultValue = 'ID and Name'
		 # + '. \nTable: '+ table
	elif (lookFor == 'employee'):
		defaultValue = 'ID and Name'
		 # + '. \nTable: '+ table
	elif (table == 'transactions_table'):
		lookFor = lookFor.upper()
		if transactions_table[lookFor]:
			defaultValue = transactions_table[lookFor]
	return defaultValue


def findTable(lookingFor):

	table = ''

	# print lookingFor
	if lookingFor != None:
		lookingFor = lookingFor.lower()
		if lookingFor == 'component':
			table = 'components_table'
		elif lookingFor == 'employee':
			table = 'programmers_table'
		elif lookingFor == 'transaction':
			table = 'transactions_table'
	return table

# def findField(field):
# 	if field in components_table:
# 		return 'components_table'
	
def createRelations(allWords, what, tables):
	foundTables = set()
	def_vals = []
	for w in allWords:
		w1 = en.noun.singular(w)
		table = findTable(w1)
		if table!= '':
			foundTables.add(table)
			def_vals.append(checkDB(w1,table))

	return foundTables, def_vals






