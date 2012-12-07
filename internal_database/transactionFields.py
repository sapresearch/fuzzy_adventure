
def get_transaction_number(transaction):
	return transaction['Pointers']


def get_transaction_component(transaction):
	return transaction['Component']

	
def get_transaction_processor(transaction):
	return transaction['Processor']
	
	
def get_transaction_start_date(transaction):
	return transaction['Sent date']
	
	
def get_transaction_end_date(transaction):
	return transaction['Completed']
	
	
def get_transaction_status(transaction):
	return transaction['Status']

	
def get_transaction_priority(transaction):
	return transaction['Priority']