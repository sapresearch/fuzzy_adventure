from sys import argv
from transactionsParser import *

script, file_name = argv


transactions = get_transactions(file_name)


#for transaction in transactions:
sections = separate_sections(transactions[0])

transaction_number = get_transaction_number(sections)
short_text = get_short_text(sections)
system = get_system(sections)
message_attributes = get_message_attributes(sections)
description = get_description(sections)
messages = get_messages(sections)


transaction_content = {
					"Transaction number": transaction_number,
					"Short Text": short_text,
					"System": system,
					"Message attributes": message_attributes,
					"Description": description,
					"Messages": messages}
for key, value in transaction_content.items():
	if (key == "Messages"):
		for message in messages:
			for key, value in message.items():
				print key, value
	else:
		print '\n', key.upper(),'\n', value
