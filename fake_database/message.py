import random

class Message(object):
	
	def get_new_message(self):
		self.text_body = 'Maybe generate random text with N-gram based on Brown Corpus'
		self.programmer_to = random.randint(1,300)
		self.customer_from = random.randint(1,300)
		self.bug_id = random.randint(1,500)
		self.reply_id = random.randint(1,300)
		
		return self
		
		
		
		messages (text_body, programmer_to, customer_from, bug_id, reply_id)