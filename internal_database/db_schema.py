import MySQLdb
from utility import *

def create_db_schema(db, delete = False):
	if(delete):
		delete_persistence(delete)
		drop_tables(db)
		create_transactions_table(db)
		create_programmers_table(db)
		create_messages_table(db)
		create_components_table(db)

	
def drop_tables(db):
	db.query("DROP TABLE IF EXISTS transactions")
	db.query("DROP TABLE IF EXISTS programmers")
	db.query("DROP TABLE IF EXISTS messages")
	db.query("DROP TABLE IF EXISTS components")
	print("Tables 'transactions, programmers, messages, components' droped from the database")
	
def create_transactions_table(db):
	sql = """CREATE TABLE transactions( 
		id             INT NOT NULL AUTO_INCREMENT, 
		trans_number   VARCHAR(50), 
		programmer_id  INT, 
		recipient      VARCHAR(30), 
		sender         VARCHAR(30), 
		short_text     TEXT, 
		client         VARCHAR(100), 
		system_release VARCHAR(30), 
		system         VARCHAR(30), 
		priority       VARCHAR(30), 
		language       VARCHAR(30), 
		status         VARCHAR(30), 
		component_id   INT, 
		description    TEXT, 
		message_id     INT, 
		PRIMARY KEY (id), 
		FOREIGN KEY (programmer_id) REFERENCES programmers(id), 
		FOREIGN KEY (component_id) REFERENCES components(id), 
		FOREIGN KEY (message_id) REFERENCES messages(id))""" 
	db.query(sql)
	print("Table 'transactions' created")


def create_programmers_table(db):
	sql = """CREATE TABLE programmers( 
		id   INT NOT NULL AUTO_INCREMENT, 
		name VARCHAR(80), 
		PRIMARY KEY (id)) """
	db.query(sql)
	print("Table 'programmers' created")


def create_messages_table(db):
	sql = """CREATE TABLE messages( 
		id       INT NOT NULL AUTO_INCREMENT, 
		type     VARCHAR(30), 
		author   VARCHAR(100), 
		date     DATE, 
		body     TEXT, 
		reply_id INT, 
		PRIMARY KEY (id), 
		FOREIGN KEY (reply_id) REFERENCES messages(id)) """
	db.query(sql)
	print("Table 'messages' created")


def create_components_table(db):
	sql = """CREATE TABLE components( 
		id   INT NOT NULL AUTO_INCREMENT, 
		name VARCHAR(30), 
		PRIMARY KEY (id)) """
	db.query(sql)
	print("Table 'components' created")

