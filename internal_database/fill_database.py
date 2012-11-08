from db_schema import *
from transactions import *
from sys import argv
from utility import *
from datetime import datetime
import time

script, file_name = argv

db = MySQLdb.connect(host="localhost",user="root",passwd="",db="batcave")

create_db_schema(db)

transactions = Transaction.load_transactions(file_name)

def insert_transaction(transaction):

		transaction_number = transaction.transaction_number
		
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

		db.query(sql)


def insert_programmer(programmer):
	sql = """SELECT id FROM programmers WHERE name = '%s'""" % programmer
	db.query(sql)
	rows = db.store_result().fetch_row(0)
	# If not already in the database, insert it
	if len(rows) == 0:
		sql = """INSERT INTO programmers (name) VALUES ('%s')""" % programmer
		db.query(sql)
		return db.insert_id()
	# If already in the database, return its id
	elif len(rows) == 1:
		row_tuple = rows[0]
		return row_tuple[0]
	else:
		print "Duplicate programmer found in the database. This should not happen since we assume that all programmers have different names"
		

def insert_component(component):
	sql = """SELECT id FROM components WHERE name = '%s'""" % component
	db.query(sql)
	rows = db.store_result().fetch_row(0)
	# If not already in the database, insert it
	if len(rows) == 0:
		sql = """INSERT INTO components (name) VALUES ('%s')""" % component
		db.query(sql)
		return db.insert_id()
	# If already in the database, return its id
	elif len(rows) == 1:
		row_tuple = rows[0]
		return row_tuple[0]
	else:
		print "Duplicate component found in the database. This should not happen since we assume that all programmers have different names"
		
	
def insert_messages(messages):
	# messages is an array of dictionnary containing the information of every message
	#raw_input(messages)
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


# LOADING FROM FILE TEST
start = time.time()
programmers = []
components = []
for transaction in transactions:
	programmer_name = transaction.message_attributes['Processor']
	programmers.append(camel_case(programmer_name))
	
	component_name = transaction.message_attributes['Component']
	components.append(component_name)
	
programmers = set(programmers)
components = set(components)

print "%f seconds to extract %d programmers and %d components in a set" \
% ((time.time() - start), len(programmers), len(components))


# INSERTING IN DB
start = time.time()
end_time_trans = None

for transaction in transactions:
	insert_transaction(transaction)
	end_time_trans = time.time()
	

	
# TEST 
db.query("""SELECT * FROM transactions""")
rows = db.store_result().fetch_row(0)

print "%f seconds to load %d transactions in the database"\
% ((end_time_trans - start), len(rows))
	
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