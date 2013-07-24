import json
from json import *

config_file = open('config.txt').read()
configuration = json.loads(config_file)
	
def get_nb_programmers():
	return configuration['programmers']
	
def get_nb_teams():
	return configuration['teams']
	
def get_nb_bugs():
	return configuration['bugs']
	
def get_nb_softwares():
	return configuration['softwares']
	
def get_nb_messages():
	return configuration['messages']
	
def get_nb_customers():
	return configuration['customers']


