import random

class RandomTeam(object):
	
	count = 0
	created_team = []
	
	def __init__(self):
		RandomTeam.count += 1
		self.id = RandomTeam.count
		self.manager = 'John'
		self.super_team_id = random.randint(1,5)
		RandomTeam.created_team.append(self)