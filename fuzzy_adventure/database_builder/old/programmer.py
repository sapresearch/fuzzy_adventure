import random


first_names = []
last_names = []

def load_first_names():
	for first_name in open('firstNames.txt', 'r').readlines():
		first_names.append(first_name.strip())
		
def load_last_names():
	for last_name in open('lastNames.txt', 'r').readlines():
		last_names.append(last_name.strip())

load_first_names()
load_last_names()

class RandomProgrammer(object):
	count = 0
	created_programmers = []
	
	def __init__(self):
		RandomProgrammer.count += 1
		self.id = RandomProgrammer.count
		self.first_name = first_names[random.randint(0,599)]
		self.last_name = last_names[random.randint(0,599)]
		self.team_id = random.randint(1,10)	
		RandomProgrammer.created_programmers.append(self)