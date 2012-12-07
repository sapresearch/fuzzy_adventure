import MySQLdb
from persistence_manager import *

def create_db_schema(db, delete = False):
	if(delete):
		delete_persistences(delete)
		drop_tables(db)
		create_transactions_table(db)
		create_programmers_table(db)
		create_components_table(db)

	
def drop_tables(db):
	db.query("DROP TABLE IF EXISTS transactions")
	db.query("DROP TABLE IF EXISTS programmers")
	db.query("DROP TABLE IF EXISTS components")
	print("Tables 'transactions, programmers, components' droped from the database")
	
def create_transactions_table(db):
	sql = """CREATE TABLE transactions( 
		id             INT NOT NULL AUTO_INCREMENT, 
		trans_number   VARCHAR(50), 
		programmer_id  INT, 
		start_date     DATE, 
		end_date	   DATE,
		status         VARCHAR(30), 
		priority	   VARCHAR(20),
		component_id   INT, 
		PRIMARY KEY (id), 
		FOREIGN KEY (programmer_id) REFERENCES programmers(id), 
		FOREIGN KEY (component_id) REFERENCES components(id))""" 
	db.query(sql)
	print("Table 'transactions' created")


def create_programmers_table(db):
	sql = """CREATE TABLE programmers( 
		id   INT NOT NULL AUTO_INCREMENT, 
		name VARCHAR(80), 
		PRIMARY KEY (id)) """
	db.query(sql)
	print("Table 'programmers' created")


def create_components_table(db):
	sql = """CREATE TABLE components( 
		id   INT NOT NULL AUTO_INCREMENT, 
		name VARCHAR(30), 
		PRIMARY KEY (id)) """
	db.query(sql)
	print("Table 'components' created")

