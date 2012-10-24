import random
from configuration import *

PROGRAMMERS = get_nb_programmers()
BUGS = get_nb_bugs()
MESSAGES = get_nb_messages()
CUSTOMERS = get_nb_customers()

class RandomMessage(object):
	count = 0
	created_messages = []
	
	def __init__(self):
		RandomMessage.count += 1
		self.id = RandomMessage.count
		self.text_body = 'Maybe generate random text with N-gram based on Brown Corpus'
		self.programmer_to = random.randint(1, PROGRAMMERS)
		self.customer_from = random.randint(1, CUSTOMERS)
		self.bug_id = random.randint(1, BUGS)
		self.reply_id = random.randint(1, MESSAGES)
		RandomMessage.created_messages.append(self)
		