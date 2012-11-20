from section import *
from utility import *
import time


LINE_SEPARATOR = ("%s%s%s") % ('\n', '_' * 72 ,'\n')
class Transaction(object):

	def __init__(self):
		self.transaction_number = None
		self.origins = None
		self.short_text = None
		self.system = None
		self.message_attributes = None
		self.description = None
		self.messages = None
		
	@staticmethod
	def load_transactions(file_name):
		start = time.time()
		transactions = []
		for transaction_to_parse in Transaction.get_transactions(file_name):
			sections = separate_sections(transaction_to_parse)

			transaction_number = get_transaction_number(sections)
			origins = get_origins(sections)
			short_text = get_short_text(sections)
			system = get_system(sections)
			message_attributes = get_message_attributes(sections)
			description = get_description(sections)
			messages = get_messages(transaction_to_parse)

			transaction = Transaction()
			transaction.transaction_number = transaction_number
			transaction.origins = origins
			transaction.short_text = short_text
			transaction.system = system
			transaction.message_attributes = message_attributes
			transaction.description = description
			transaction.messages = messages
			
			transaction_content = {
							"Transaction number": transaction_number,
							"Origins": origins,
							"Short Text": short_text,
							"System": system,
							"Message attributes": message_attributes,
							"Description": description,
							"Messages": messages}
			
			transactions.append(transaction)
			
		print "%s to load %d transactions from the file: %s"\
		% (pretty_print_duration(time.time() - start), len(transactions), file_name)
		return transactions
		

	@staticmethod
	def get_transactions(file_name):
		regex = re.compile('[\r\n]{2,4}(R\/3 Internal Message: )(.{26})[\r\n]{2,4}_{72}')
		file = open(file_name).read()
		splits = re.split(regex, file)

		# Pop the first item because it's empty. The very first line of a file
		splits.pop(0)
		numbers = [splits[i] for i in range(len(splits)) if i % 3 == 1]
		bodies = [splits[i] for i in range(len(splits)) if i % 3 == 2]
	

		transactions = [numbers[i] + '\n' + ('_' * 72) + bodies[i] for i in range(len(numbers))]

		return transactions

	
		
	def __str__(self):
		string = ""
		string += '\n\n***** TRANSACTION NUMBER *****\n'
		string += self.transaction_number
		string += '\n\n***** ORIGINS *****\n'
		string += str(self.origins)
		string += '\n\n***** SHORT TEXT *****\n'
		string += self.short_text
		string += '\n\n***** SYSTEM *****\n'
		string += str(self.system)
		string += '\n\n***** TRANSACTION ATTRIBUTES *****\n'
		string += str(self.message_attributes)
		string += '\n\n***** DESCRIPTION *****\n'
		string += self.description
		
		for message in self.messages:
			string += "%-20s %-20s %-20s\n" % ("TYPE", "AUTHOR", "TIME")
			string += "%-20s %-20s %-20s\n\n" %(
										message['Type'], 
										message['Author'], 
										message['Time'])
			string += message['Message']
			string += LINE_SEPARATOR
			
		return string
			