from persistence import *


transactions_path = 'persistence/transactions_treated.p'
programmers_path = 'persistence/programmers_treated.p'
components_path = 'persistence/components_treated.p'

transactions_persistence = None
programmers_persistence = None
components_persistence = None


def set_persistences(database):
	global transactions_persistence, programmers_persistence, components_persistence
	
	if transactions_persistence == None:
		transactions_persistence = CounterPersistence(database, transactions_path)
		
	if programmers_persistence == None:
		programmers_persistence = CounterPersistence(database, programmers_path)
	
	if components_persistence == None:
		components_persistence = CounterPersistence(database, components_path)


def load_persistences():

	
	transactions_treated = transactions_persistence.load()
	programmers_treated = programmers_persistence.load()
	components_treated = components_persistence.load()
		
	return transactions_treated, programmers_treated, components_treated


def dump_persistences():

	
	try:
		transactions_persistence.dump()
		programmers_persistence.dump()
		components_persistence.dump()

	except pickle.PickleError:
		print "A problem occured with dumping the persistance. A fresh new import is required."


def delete_persistences(delete = False):

	transactions_persistence.delete(delete)
	programmers_persistence.delete(delete)
	components_persistence.delete(delete)	
	

def update_persistences(db, update = False):
	"""Update all the persistence objects to align them with the database"""

	
	transactions_persistence.update(db, 'trans_number', 'transactions', update)
	programmers_persistence.update(db, 'name', 'programmers', update)
	components_persistence.update(db, 'name', 'components', update)	