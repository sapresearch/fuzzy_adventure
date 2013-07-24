import os
import MySQLdb
import pickle
import numpy as np


def load(file_name):
	"""A loaded persistence must be subsequently dumped in order to keep the modifications."""
	try:
		file = open(file_name, 'rb')
		persistence = pickle.load(file)
		file.close()
	except IOError:
		persistence = []
		
	return persistence
	
	
def dump(persistence, file_name):
	"""Dump the persistence in the file. Load must be called before in order to have something to dump."""
	try:
		file = open(file_name, 'wb')
		pickle.dump(persistence, file)
		# Make it none accessible after dumping it. Forcing the use of load() afterward
		file.close()
	except pickle.PickleError:
		print "A problem occured with dumping the persistance.\
		Run again with '-d' or '-u'."
