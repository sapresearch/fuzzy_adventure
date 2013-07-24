
import _mysql
from _mysql import *

server_connection = None


def listDatabases():
	"""Lists all the databases in the localhost"""
	open_server_connection()
	print "Using server_connection: ", server_connection
	server_connection.query("""SHOW DATABASES;""")
	databases = server_connection.store_result().fetch_row(0)
	for i in range(0, len(databases)):
		print i, databases[i]
	close_server_connection()
	
def query(query):
	"""Sends the query to the localhost"""
	open_server_connection()
	server_connection.query(query)
	result = server_connection.store_result()
	if result != None:
		result = result.fetch_row(0)
	close_server_connection()
	return result
	
def open_server_connection():
	global server_connection
	if server_connection == None:
		server_connection = _mysql.connect(host="localhost",user="root",passwd="")

def close_server_connection():
	global server_connection
	server_connection.close()
	server_connection = None
	
def create_table(database, table):
	open_server_connection()
	# TODO Check if database is a string and if the query worked
	server_connection.query("""USE %s;""" % database)
	# TODO Check if table_name is a string and if the query worked
	server_connection.query("""CREATE TABLE %s (Id int);""" % table)
	
def add_column(database, table, column, data_type):
	open_server_connection()
	# TODO Check if database is a string and if the query worked
	server_connection.query("""USE %s;""" % database)
	# TODO Check if table_name is a string and if the query worked
	server_connection.query("""ALTER TABLE %s ADD %s %s;""" % (table, column, data_type))

def make_primary_key(database, table_name, column):
	open_server_connection()
	# TODO Check if database is a string and if the query worked
	server_connection.query("""USE %s;""" % database)
	# TODO Check if table_name is a string and if the query worked
	server_connection.query("""ALTER TABLE %s ADD PRIMARY KEY (%s);""" % (table, column))

def listTables(database):
	open_server_connection()
	# TODO Check if database is a string and if the query worked
	server_connection.query("""USE %s;""" % database)
	# TODO Check if table_name is a string and if the query worked
	server_connection.query("""SHOW TABLES""")
	
	tables = server_connection.store_result().fetch_row(0)
	for i in range(0, len(tables)):
		print i, tables[i]
	close_server_connection()
