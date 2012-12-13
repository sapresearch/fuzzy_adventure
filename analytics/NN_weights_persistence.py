import os
import MySQLdb
import pickle
import numpy as np


def load():
	"""A loaded persistence must be subsequently dumped in order to keep the modifications."""
	try:
		file = open('NN_weights.p', 'rb')
		persistence = pickle.load(file)
		file.close()
	except IOError:
		persistence = []

	return persistence
	
	
def dump(persistence):
	"""Dump the persistence in the file. Load must be called before in order to have something to dump."""
	try:
		file = open('NN_weights.p', 'wb')
		pickle.dump(persistence, file)
		# Make it none accessible after dumping it. Forcing the use of load() afterward
		file.close()
	except pickle.PickleError:
		print "A problem occured with dumping the persistance.\
		Run again with '-d' or '-u'."
		
		

