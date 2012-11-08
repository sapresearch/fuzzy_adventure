from sys import argv
from transactionsParser import *
import time


start = time.time()

script, file_name = argv

def print_transaction(transaction):
	for key, value in transaction.items():
		if (key == "Messages"):
			for message in transaction[key]:
				print "%-20s %-20s %-20s" % ("TYPE", "AUTHOR", "TIME")
				print "%-20s %-20s %-20s" %(
											message['Author'], 
											message['Type'], 
											message['Time'])
				print message['Message']
				print '_' * 72
		else:
			print '\n*****', key.upper(),'*****\n', value
		raw_input("_" * 72)
			

transactions = []
for transaction in get_transactions(file_name):
	sections = separate_sections(transaction)

	
	transaction_number = get_transaction_number(sections)
	origins = get_origins(sections)
	#print len(transactions), transaction_number
	short_text = get_short_text(sections)
	system = get_system(sections)
	message_attributes = get_message_attributes(sections)
	description = get_description(sections)
	messages = get_messages(sections)

	transaction_content = {
					"Transaction number": transaction_number,
					"Origins": origins,
					"Short Text": short_text,
					"System": system,
					"Message attributes": message_attributes,
					"Description": description,
					"Messages": messages}
	
	transactions.append(transaction_content)

print "%d transactions read in file" % len(transactions)

print "TOTAL TIME %f seconds" % (time.time() - start)