from db_schema import *
from transactions import *
from sys import argv
from utility import *
from datetime import datetime
import time
import MySQLdb
import os
import argparse
from persistence_manager import *

# Easier on the eye to print an empty line after the command line
print ""

def main():
	if (not os.path.exists(directory_name)):
		raise NameError('This path does not exists')
	
	file_list = []
	# If the path provided is a directory, get a list of what's inside
	if (os.path.isdir(directory_name)):
		file_list = os.listdir(directory_name)
		
	else:
		raise NameError('%s is not a valid directory' % directory_name)
	
	print "\n%d file(s) to import" % len(file_list)
	for file in file_list:
		print "\t-  %s" % file
	print ""
	
	for file in file_list:
		path = os.path.join(directory_name, file)
		if (not os.path.isfile(path)):
			print "File '%s' cannot be read because it's not a file\n" % file
			continue
		print "Loading transactions from %s" % path
		try:
			transactions = Transaction.load_transactions(path)
			insert_all_transactions(transactions)
		except Exception as e:
			print "An error occured while treating the file %s." % path
			print type(e)
			print e.args
			print ""



def insert_all_transactions(transactions):
	count = 0
	start_count = time.time()
	nb_transactions = len(transactions)
	for transaction in transactions:
		insert_transaction(transaction)
		count += 1
		print "\t%d%% completed\r" % ((count * 100 / nb_transactions)),

	print "%s to complete the insertion process.\n" % pretty_print_duration(time.time() - start_count)

	
def insert_transaction(transaction):
	
	transaction_number = transaction.trans_number
	# Increment the count of the transaction for futur reference
	transactions_treated[transaction_number] += 1
	
	# Find out if a transaction number has already be treated
	if transactions_treated[transaction_number] > 1:
		# If so, the early return
		return None

	programmer = camel_case(transaction.processor)
	programmer = escape_string(programmer)
	programmer_id = insert_programmer(programmer)
	
	start_date = transaction.start_date
	end_date = transaction.end_date
	status = escape_string(transaction.status)
	priority = transaction.priority
	contract_priority = transaction.contract_priority
	product = transaction.product
	os = transaction.os
	system_type = transaction.system_type
	component = escape_string(transaction.component)
	component_id = insert_component(component)

	sql = \
		"""INSERT INTO transactions 
					(trans_number, 
					programmer_id,
					start_date,
					end_date,
					status,
					priority,
					contract_priority,
					product,
					os,
					system_type,
					component_id) 
		VALUES      ('%s', %d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %d)""" \
					%(transaction_number, \
					programmer_id, \
					start_date, \
					end_date, \
					status,  \
					priority, \
					contract_priority, \
					product, \
					os, \
					system_type, \
					component_id)

	try:
		db.query(sql)
	except MySQLdb.ProgrammingError:
		print "Transaction %s could not be inserted" % transaction_number
		print "Query used: %s" % sql


def insert_programmer(programmer):
	programmers_treated[programmer] += 1
	
	if programmers_treated[programmer] > 1:
		sql = """SELECT id FROM programmers WHERE name = '%s'""" % programmer
		db.query(sql)
		row = db.store_result().fetch_row()
		return row[0][0]

	sql = """INSERT INTO programmers (name) VALUES ('%s')""" % programmer
	db.query(sql)
	return db.insert_id()


def insert_component(component):
	components_treated[component] += 1

	if components_treated[component] > 1:
		sql = """SELECT id FROM components WHERE name = '%s'""" % component
		db.query(sql)
		row = db.store_result().fetch_row()
		return row[0][0]
		
	sql = """INSERT INTO components (name) VALUES ('%s')""" % component
	db.query(sql)
	return db.insert_id()

	
update, delete, directory_name, database = arguments_parser()
db = MySQLdb.connect(host="localhost", user="root", passwd="nolwen", db=database)
set_persistences(database)

# INSERTING IN DB
create_db_schema(db, delete)

try:
	update_persistences(db, update)
except OSError as ose:
	print ose
	exit()

transactions_treated, programmers_treated, components_treated = load_persistences()
start = time.time()
main()
total_time = (time.time() - start)
dump_persistences()


print "%s to complete the entire process" % pretty_print_duration(total_time)
# TEST 
print_stats(db)


db.close()