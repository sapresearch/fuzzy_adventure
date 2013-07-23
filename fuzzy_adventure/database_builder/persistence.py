import os
import MySQLdb
import pickle
from collections import Counter

class CounterPersistence(object):
	database = ""
	basepath = ""
	persistence = None
	
	def __init__(self, database, path):
		self.database = database
		self.basepath = path
	

	def path(self):
		"""Returns the path of the persistence file on disk."""
		basename = os.path.basename(self.basepath)
		new_basename = self.database + '_' + basename
		dirname = os.path.dirname(self.basepath)
		if not os.path.exists(dirname):
			os.makedirs(dirname)
		
		full_path = os.path.join(dirname, new_basename)
		return full_path
		
		
	def load(self):
		"""A loaded persistence must be subsequently dumped in order to keep the modifications."""
		try:
			file = open(self.path(), 'rb')
			self.persistence = pickle.load(file)
			print "-> '%s' loaded from file" % self.path()
			file.close()
		except IOError:
			self.persistence = Counter()

		return self.persistence
		
		
	def dump(self):
		"""Dump the persistence in the file. Load must be called before in order to have something to dump."""
		try:
			file = open(self.path(), 'wb')
			pickle.dump(self.persistence, file)
			# Make it none accessible after dumping it. Forcing the use of load() afterward
			self.persistence = None
			file.close()
		except pickle.PickleError:
			print "A problem occured with dumping the persistance.\
			Run again with '-d' or '-u'."
			
			
	def delete(self, delete = False):
		"""Delete the persistence object on the disk."""
		if delete and os.path.exists(self.path()):
			try: 
				os.remove(self.path())
				self.persistence = None
			except OSError:
				print "Could not delete the persistence %s" % self.path()
				raise OSError


	def update(self, db, field, table, update = False):
		"""Update the persistence object to align it with the database.
		This requires the table and the field name to match it with."""
		
		if not update:
			return None
		# Delete the old persistence object
		self.delete(True)

		# Update transactions treated
		self.persistence = Counter()
		db.query("""SELECT %s FROM %s""" %(field, table))
		rows = db.store_result().fetch_row(0)
		for row in rows:
			self.persistence[row[0]] += 1

		self.dump()
		# TODO if dumping fails, this will print. Add robustness
		print "-> Persistence '%s' updated" % self.path()
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
