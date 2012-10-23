import random

class Team(object):
	
	def get_new_team(self):
		new_team = Team()
		new_team.manager = 'John'
		new_team.super_team_id = random.randint(1,5)
		return new_team