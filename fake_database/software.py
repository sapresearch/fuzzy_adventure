import random

class RandomSoftware(object):
	
	count = 0
	created_softwares = []
	
	def __init__(self):
		RandomSoftware.count += 1
		self.id = RandomSoftware.count
		self.super_software_id = random.randint(1,10)
		RandomSoftware.created_softwares.append(self)