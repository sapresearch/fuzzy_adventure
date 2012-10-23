import random

class Software(object):
	
	def get_new_software(self):
		self.super_software_id = random.randint(1,10)
		return self