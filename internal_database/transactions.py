import transactionFields as tf
from utility import *
import time
import rawTransactions as rt

class Transaction(object):

	def __init__(self):
		self.trans_number = None
		self.processor = None
		self.component = None
		self.start_date = None
		self.end_date = None
		self.status = None 
		self.priority = None

		
	@staticmethod
	def load_transactions(file_name):
		start = time.time()
		transactions = []
		raw_transactions = rt.import_transactions_from_file(file_name)
		for raw_transaction in raw_transactions:
			# Get the information we need from the raw transaction
			trans_number = tf.get_transaction_number(raw_transaction)
			processor = tf.get_transaction_processor(raw_transaction)
			component = tf.get_transaction_component(raw_transaction)
			start_date = tf.get_transaction_start_date(raw_transaction)
			end_date = tf.get_transaction_end_date(raw_transaction)
			status = tf.get_transaction_status(raw_transaction)
			priority = tf.get_transaction_priority(raw_transaction)
			
			# Create the object
			transaction = Transaction()
			transaction.trans_number = trans_number
			transaction.processor = processor
			transaction.component = component 
			transaction.start_date = start_date 
			transaction.end_date = end_date 
			transaction.status = status 
			transaction.priority = priority

			# Add the objects to the transactions list
			transactions.append(transaction)
			
		print "%s to load %d transactions from the file: %s"\
		% (pretty_print_duration(time.time() - start), len(transactions), file_name)
		return transactions


	def __str__(self):
		string = ""
		string += '\n\n***** TRANSACTION NUMBER *****\n'
		string += self.trans_number
		string += '\n\n***** COMPONENT *****\n'
		string += self.component
		string += '\n\n***** START DATE *****\n'
		string += str(self.start_date)
		string += '\n\n***** END DATE *****\n'
		string += str(self.end_date)
		string += '\n\n***** STATUS *****\n'
		string += self.status
		
		return string
			