import MySQLdb as mdb
import pickle
from collections import Counter
import os
import argparse
from persistence import *

	
def escape_string(string):
	return str(mdb.escape_string(string))
	
	
def camel_case(string):
	return  ' '.join(i.capitalize() for i in string.split(' '))
	
	
def pretty_print_duration(duration):

	days = int(duration / 3600 / 24)
	duration = duration - days * 3600 * 24

	hours = int(duration / 3600)
	duration = duration - hours * 3600

	minutes = int(duration / 60)
	duration = duration - minutes * 60

	seconds = duration
	
	pretty = ""
	if days > 0:
		pretty = "%d day(s) " % days
	if hours > 0 or days > 0:
		pretty += "%d hour(s) " % hours
	if minutes > 0 or hours > 0 or days > 0:
		pretty += "%d minute(s) " % minutes
	if seconds > 0 or minutes > 0 or hours > 0 or days > 0:
		pretty += "%d second(s)" % seconds

	return pretty
	

	
def print_stats(db):
	db.query("""SELECT * FROM transactions""")
	rows = db.store_result().fetch_row(0)
	print "\n%d transactions in the database" % (len(rows))

	db.query("""SELECT * FROM programmers""")
	rows = db.store_result().fetch_row(0)
	print "%d programmers in the database" % len(rows)

	db.query("""SELECT * FROM components""")
	rows = db.store_result().fetch_row(0)
	print "%d components in the database" % len(rows)

	
	
def arguments_parser():
	parser = argparse.ArgumentParser()
	group = parser.add_mutually_exclusive_group()
	
	group.add_argument('-u', action='store_true', default = False, \
		help="""Update the persistence lists of the informations in the database. 
		Use in case you suspect the database is not up-to-date.""")
		
	group.add_argument('-d', action='store_true', default = False,\
		help='Delete the database and start from scratch.')
		
	parser.add_argument('-directory', required=True, \
	help='The directory containing the files to import in the database.')
	
	parser.add_argument('-database', default='batcave', \
	help='The database in which to perform the import of all transactions.')
	
	args = parser.parse_args()	

	update = args.u
	delete = args.d
	directory_name = args.directory
	database = args.database
	
	return update, delete, directory_name, database
	
	
def open_database(database):
	return mdb.connect(host="localhost", user="root", passwd="", db=database)