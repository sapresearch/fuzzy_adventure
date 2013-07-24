import random
import time
from datetime import date, timedelta
from configuration import *
from programmer import *

PROGRAMMERS = get_nb_programmers()
SOFTWARES = get_nb_softwares()
CUSTOMERS = get_nb_customers()


class RandomBug(object):
	count = 0
	created_bugs = []
	
	def __init__(self):
		RandomBug.count += 1
		self.id = RandomBug.count
		self.start_date = self.random_date_from(date(1990,1,1)) # Arbitrary start date
		self.close_date = self.random_close_date_from(self.start_date)
		self.customer_id = random.randint(1, CUSTOMERS)
		self.software_id = random.randint(1,SOFTWARES)
		self.programmer_id = random.randint(1, PROGRAMMERS)
		self.description = 'Bug description. Maybe generate random text with trigram from Brown Corpus'

	def random_close_date_from(self, date):
		close_date = self.random_date_from(date)
		if(random.random() < 0.2):
			close_date = None
		return close_date
		
	def random_date_from(self, date):
		delta = date.today() - date
		return date + timedelta(random.randint(0, delta.days))
		
