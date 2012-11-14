from db_schema import *
from transactions import *
from sys import argv
from utility import *
from datetime import datetime
from collections import Counter
import time
import _mysql as mdb
import os


script, directory_name = argv
db = MySQLdb.connect(host="localhost",user="root",passwd="",db="batcave")
create_db_schema(db)
transactions_treated = Counter()
programmers_treated = Counter()
components_treated = Counter()

def main():
	if (not os.path.exists(directory_name)):
		raise NameError('This path does not exists')
	
	file_list = []
	# If the path provided is a directory, get a list of what's inside
	if (os.path.isdir(directory_name)):
		file_list = os.listdir(directory_name)
		
	# If the path provided is a file, append it to the file list
	else:
		raise NameError('%s is not a valid directory' % directory_name)
	
	print "\n%d files to import" % len(file_list)
	for file in file_list:
		print "\t-  %s" % file
	print ""
	
	for file in file_list:
		path = os.path.join(directory_name, file)
		if (not os.path.isfile(path)):
			print "File %s cannot be read because it's not a file" % file
			continue
		print "Loading transactions from %s" % path
		transactions = Transaction.load_transactions(path)
		insert_all_transactions(transactions)


def insert_all_transactions(transactions):
	count = 0
	start_count = time.time()
	nb_transactions = len(transactions)
	for transaction in transactions:
		insert_transaction(transaction)
		count += 1
		print "\t%d%% completed\r" % (count * 100 / nb_transactions),

	print "%s to complete the insertion process.\n" % pretty_print_duration(time.time() - start_count)

	
def insert_transaction(transaction):

	transaction_number = transaction.transaction_number
	# Increment the count of the transaction for futur reference
	transactions_treated[transaction_number] += 1
	
	# Find out if a transaction number has already be treated
	if transactions_treated[transaction_number] > 1:
		# If so, the early return
		return None

	programmer = camel_case(transaction.message_attributes['Processor'])
	programmer = escape_string(programmer)
	programmer_id = insert_programmer(programmer)
	
	recipient = escape_string(transaction.origins['Recipient'])
	sender = transaction.origins['Sender']
	short_text = escape_string(transaction.short_text)
	client = transaction.system['Client']
	system_release = transaction.system['Release']
	system = transaction.system['System']
	priority = transaction.message_attributes['Priority']
	language = transaction.message_attributes['Language']
	status = transaction.message_attributes['Status']
	
	component = transaction.message_attributes['Component']
	component_id = insert_component(component)
	
	description = escape_string(transaction.description)
	message_id = insert_messages(transaction.messages) #Fill Messages table first
	
	sql = \
		"""INSERT INTO transactions 
					(trans_number, 
					programmer_id,
					recipient, 
					sender, 
					short_text, 
					client, 
					system_release, 
					system, 
					priority, 
					language, 
					status,
					component_id,
					description,
					message_id) 
		VALUES      ('%s', %d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %d, '%s', %d)""" \
					%(transaction_number, \
					programmer_id, \
					recipient, \
					sender, \
					short_text, \
					client, \
					system_release, \
					system, \
					priority, \
					language, \
					status,  \
					component_id, \
					description, \
					message_id)

	try:
		db.query(sql)
	except ProgrammingError:
		print "Transaction %s could not be inserted" % transaction_number


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

	
def insert_messages(messages):
	# messages is an array of dictionnary containing the information of every message
	if(len(messages) == 0):
		return -1
	
	message = messages[0]
	
	sql = create_single_message_query(message)
	db.query(sql)
	first_message_id = db.insert_id()
	previous_insertion_id = first_message_id

	for i in range(1, len(messages)):
		message = messages[i]
		sql = create_single_message_query(message)
		db.query(sql)
		
		# Update the parent message with the reply_id
		reply_id = db.insert_id()
		sql = """UPDATE messages SET reply_id=%d WHERE id=%d""" % (reply_id, previous_insertion_id)
		db.query(sql)
		
		# Make the currently inserted message the previous_insertion_id
		previous_insertion_id = reply_id
	
	return first_message_id


def create_single_message_query(message):
	# reply_id is left out. It will be added in insert_messages
	
	type = message['Type']
	
	author = message['Author']
	author = escape_string(camel_case(author))

	date = message['Date']
	if date == '':
		print message
	date = datetime.strptime(date,"%d.%m.%Y %H:%M:%S")
		
	body = escape_string(message['Body'])
	
	sql = \
		"""INSERT INTO messages 
					(type, author, date, body) 
		VALUES		('%s', '%s', '%s', '%s')""" \
					%(type, \
					author, \
					date, \
					body)

	return sql

	
# INSERTING IN DB
start = time.time()
main()
total_time = (time.time() - start)


# TEST 
db.query("""SELECT * FROM transactions""")
rows = db.store_result().fetch_row(0)
print "%s to load %d transactions in the database"\
% (pretty_print_duration(total_time), len(rows))

print "Here's a list of duplicates for your convenience"
duplicate_list = transactions_treated.most_common(10)
for duplicate in duplicate_list:
	if duplicate[1] > 1:
		print duplicate
	
db.query("""SELECT * FROM programmers""")
rows = db.store_result().fetch_row(0)
print "%d programmers inserted into the database" % len(rows)


db.query("""SELECT * FROM components""")
rows = db.store_result().fetch_row(0)
print "%d components inserted into the database" % len(rows)

db.query("""SELECT * FROM messages""")
rows = db.store_result().fetch_row(0)
print "%d messages inserted into the database" % len(rows)




db.close()