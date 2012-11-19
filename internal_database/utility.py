import MySQLdb
import pickle
from collections import Counter
import os
import argparse

transactions_path = 'persistence/transactions_treated.p'
programmers_path = 'persistence/programmers_treated.p'
components_path = 'persistence/components_treated.p'
	
def escape_string(string):
	return str(MySQLdb.escape_string(string))
	
	
def camel_case(string):
	return  ' '.join(i.capitalize() for i in string.split(' '))
	
	
def pretty_print_duration(duration):

	days = int(duration / 3600 / 24)
	duration = duration - days * 3600 * 24

	hours = int(duration / 3600)
	duration = duration - hours * 3600

	minutes = int(duration / 60)
	duration = duration - minutes * 60

	seconds = duration
	
	pretty = ""
	if days > 0:
		pretty = "%d day(s) " % days
	if hours > 0 or days > 0:
		pretty += "%d hour(s) " % hours
	if minutes > 0 or hours > 0 or days > 0:
		pretty += "%d minute(s) " % minutes
	if seconds > 0 or minutes > 0 or hours > 0 or days > 0:
		pretty += "%d second(s)" % seconds

	return pretty
	
	
def load_persistence():
	transactions_treated = None
	programmers_treated = None
	components_treated = None
	try:
		transactions_treated = pickle.load(open(transactions_path, 'rb'))
		print "\n-> Transactions treated loaded from file"
	except IOError:
		transactions_treated = Counter()

	try:
		programmers_treated = pickle.load(open(programmers_path, 'rb'))
		print "-> Programmers treated loaded from file"
	except IOError:
		programmers_treated = Counter()

	try:
		components_treated = pickle.load(open(components_path, 'rb'))
		print "-> Components treated loaded from file"
	except IOError:
		components_treated = Counter()
		
	return transactions_treated, programmers_treated, components_treated
	

def dump_persistence(transactions_treated, programmers_treated, components_treated):
	
	try:
		pickle.dump(transactions_treated, open(transactions_path, 'wb'))
		pickle.dump(programmers_treated, open(programmers_path, 'wb'))
		pickle.dump(components_treated, open(components_path, 'wb'))
	except pickle.PickleError:
		print "A problem occured with dumping the persistance. A fresh new import is required."
		
		
def delete_persistence(delete = False):
	
	if delete:
		if os.path.exists(transactions_path):
			try: 
				os.remove(transactions_path)
			except OSError:
				print "Could not delete the persistence for transactions"
				raise OSError
				
		if os.path.exists(programmers_path):
			try: 
				os.remove(programmers_path)
			except OSError:
				print "Could not delete the persistence for programmers"
				raise OSError
				
		if os.path.exists(components_path):
			try: 
				os.remove(components_path)
			except OSError:
				print "Could not delete the persistence for components"
				raise OSError


# Update the persistence objects to align them with the database
def update_persistence(db, update = False):
	if not update:
		return None
	# Delete the old persistence object
	delete_persistence(True)

	# Update transactions treated
	transactions_treated = Counter()
	db.query("""SELECT trans_number FROM transactions""")
	rows = db.store_result().fetch_row(0)
	for row in rows:
		transactions_treated[row[0]] += 1
	
	# Update programmers_treated
	programmers_treated = Counter()
	db.query("""SELECT name FROM programmers""")
	rows = db.store_result().fetch_row(0)
	for row in rows:
		programmers_treated[row[0]] += 1
	
	# Update components_treated
	components_treated = Counter()
	db.query("""SELECT name FROM components""")
	rows = db.store_result().fetch_row(0)
	for row in rows:
		components_treated[row[0]] += 1
	
	dump_persistence(transactions_treated, programmers_treated, components_treated)
	# TODO if dumping fails, this will print. Add robustness
	print "\n-> All persistence objects updated"

	
def print_stats(db):
	db.query("""SELECT * FROM transactions""")
	rows = db.store_result().fetch_row(0)
	print "\n%d transactions in the database" % (len(rows))

	db.query("""SELECT * FROM programmers""")
	rows = db.store_result().fetch_row(0)
	print "%d programmers in the database" % len(rows)

	db.query("""SELECT * FROM components""")
	rows = db.store_result().fetch_row(0)
	print "%d components in the database" % len(rows)

	db.query("""SELECT * FROM messages""")
	rows = db.store_result().fetch_row(0)
	print "%d messages in the database" % len(rows)
	
	
def arguments_parser():
	parser = argparse.ArgumentParser()
	group = parser.add_mutually_exclusive_group()
	
	group.add_argument('-u', action='store_true', default = False, \
		help="""Update the persistence lists of the informations in the database. 
		Use in case you suspect the database is not up-to-date.""")
		
	group.add_argument('-d', action='store_true', default = False,\
		help='Delete the database and start from scratch.')
		
	parser.add_argument('-directory', required=True, \
	help='The directory containing the files to import in the database.')
	
	parser.add_argument('-database', default='batcave', \
	help='The database in which to perform the import of all transactions.')
	
	args = parser.parse_args()	

	update = args.u
	delete = args.d
	directory_name = args.directory
	database = args.database
	
	return update, delete, directory_name, database