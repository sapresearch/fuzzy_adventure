import MySQLdb


def create_db_schema(db):
	create_transactions_table(db)
	create_programmers_table(db)
	create_messages_table(db)
	create_components_table(db)

	
def create_transactions_table(db):
	# Drop table if it already exist using execute() method.
	db.query("DROP TABLE IF EXISTS transactions")
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


def create_programmers_table(db):
	db.query("DROP TABLE IF EXISTS programmers")
	sql = """CREATE TABLE programmers( 
		id   INT NOT NULL AUTO_INCREMENT, 
		name VARCHAR(80), 
		PRIMARY KEY (id)) """
	db.query(sql)


def create_messages_table(db):
	db.query("DROP TABLE IF EXISTS messages")
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


def create_components_table(db):
	db.query("DROP TABLE IF EXISTS components")
	sql = """CREATE TABLE components( 
		id   INT NOT NULL AUTO_INCREMENT, 
		name VARCHAR(30), 
		PRIMARY KEY (id)) """
	db.query(sql)

