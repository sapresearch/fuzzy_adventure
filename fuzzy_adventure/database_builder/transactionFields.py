from datetime import datetime

"""
Here you add the getters you need. A transaction is fed as a dictionnary of {column title: value}. 
The column title (for the purpose of this project) comes from the text file exported from our private database.
The keys for the dictionnary (the transaction) are the headers of the columns from the text files.
"""
def get_transaction_number(transaction):
	key = 'Pointers'
	if key in transaction:
		return transaction[key]
	else:
		raise LookupError("The key '%s' could not be found.\n%r" % (key, transaction))


def get_transaction_component(transaction):
	key = 'Component'
	if key in transaction:
		return transaction[key]
	else:
		raise LookupError("The key '%s' could not be found." % key)

	
def get_transaction_processor(transaction):
	key = 'Processor'
	if key in transaction:
		return transaction[key]
	else:
		raise LookupError("The key '%s' could not be found." % key)

	
def get_transaction_start_date(transaction):
	date_key = 'Sent date'
	time_key = 'Sent Time'
	if date_key in transaction and time_key in transaction:
		date = transaction[date_key]
		time = transaction[time_key]
		date_time = date + " " + time
		return datetime.strptime(date_time,"%d.%m.%Y %H:%M:%S")
	else:
		raise LookupError("Either the key '%s' or '%s' could not be found." % (date_key, time_key))

	
def get_transaction_end_date(transaction):
	date_key = 'Completed'
	time_key = 'Completed Time'
	if date_key in transaction and time_key in transaction:
		date = transaction[date_key]
		time = transaction[time_key]
		date_time = date + " " + time
		try:
			return datetime.strptime(date_time,"%d.%m.%Y %H:%M:%S")
		except ValueError:
			pass
	else:
		raise LookupError("Either the key '%s' or '%s' could not be found." % (date_key, time_key))
	
	
def get_transaction_status(transaction):
	key = 'Status'
	if key in transaction:
		return transaction[key]
	else:
		raise LookupError("The key '%s' could not be found." % key)

	
def get_transaction_priority(transaction):
	key = 'Priority'
	if key in transaction:
		return transaction[key]
	else:
		raise LookupError("The key '%s' could not be found." % key)

	

def get_contract_priority(transaction):
	key = 'Contract Priority'
	if key in transaction:
		return transaction[key]
	else:
		raise LookupError("The key '%s' could not be found."% key)

	
def get_product(transaction):
	key = 'Product'
	if key in transaction:
		return transaction[key]
	else:
		raise LookupError("The key '%s' could not be found."% key)


def get_os(transaction):
	key = 'Operating'
	if key in transaction:
		return transaction[key]
	else:
		raise LookupError("The key '%s' could not be found."% key)

	return transaction['Operating']


def get_system_type(transaction):
	key = 'System Type'
	if key in transaction:
		return transaction[key]
	else:
		raise LookupError("The key '%s' could not be found."% key)


def get_attribute(transaction):
	key = 'Attribute'
	if key in transaction:
		return transaction[key]
	else:
		raise LookupError("The key '%s' could not be found."% key)


def get_solving_level(transaction):
	key = 'Solving Level'
	if key in transaction:
		return transaction[key]
	else:
		raise LookupError("The key '%s' could not be found."% key)


def get_24h_flag(transaction):
	key = '24h Flag'
	if key in transaction:
		return transaction[key]
	else:
		raise LookupError("The key '%s' could not be found."% key)

"""
M
Priority  
Sent date 
Sent Time 
Completed 
Completed Time
Changed on
System Type
Status                   
Number of cylces
Number of notes
Component           
Short text                                                                     
Processor           
Product        
Pointers                
Escalating
Planned Organization
Customer Calls 
Operating 
SolMan Type
System ID 
Start of Escalation 
Overrun Flag   
Active SAP Status
Escalation Type
Hold Flag 
Solving Level 
Attribute 
24h Flag  
Contract Priority   
Corporation         
Escalating Level    
Fast Track
R/3 Install. Number 
Year
"""