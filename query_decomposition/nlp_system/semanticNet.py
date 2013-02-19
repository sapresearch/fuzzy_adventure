import sys
sys.path.append("../../external")
import en

'''def required value''' 
def required_values(lookFor, allWords):
	singulars = [en.noun.singular(w.lower()) for w in allWords]
	required_values = []

	components_table =['id','name']
	transactions_table = {'ID' : 'id','TRANSACTION' : 'trans_number','PROGRAMMER' : 'programmer_id','START' : 'start_date','END' : 'end_date','STATUS' :'status','PRIORITY':'priority','CONTRACT PRIORITY' :'contract_priority','PRODUCT' : 'product','COMPONENT ID' :'component_id'}
	programmers_table = ['id','name']

	# find the table, field and default value:
	if 'components_table' in lookFor:
		required_values.append('ID and Name')
		 # + '. \nTable: '+ table
	if 'programmers_table' in lookFor:
		required_values.append('ID and Name')
		 # + '. \nTable: '+ table
	if 'transactions_table' in lookFor:
		for word in singulars:
			if word.upper() in transactions_table:
				required_values.append(transactions_table[word.upper()])
	return required_values

def tables(allWords):
	tables = []
	foundTables = set()
	singulars = [en.noun.singular(w.lower()) for w in allWords]
	table_names = {'component': 'components_table', 'employee':'programmers_table', 'transaction':'transactions_table'}
	for word,table_name in table_names.iteritems():
		if word in singulars: tables.append(table_name)
	return tables 
