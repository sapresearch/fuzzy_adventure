import random
import time
from datetime import date, timedelta

class Bug(object):
	
	def get_new_bug(self):
		self.start_date = self.random_date_from(date(1990,1,1)) # Arbitrary start date
		self.close_date = self.random_close_date_from(self.start_date)
		self.customer_id = random.randint(1,20)
		self.software_id = random.randint(1,100)
		self.programmer_id = random.randint(1,300)
		self.description = 'Bug description. Maybe generate random text with trigram from Brown Corpus'

		return self

	def random_close_date_from(self, date):
		close_date = self.random_date_from(date)
		if(random.random() < 0.2):
			close_date = None
		return close_date
		
	def random_date_from(self, date):
		delta = date.today() - date
		return date + timedelta(random.randint(0, delta.days))