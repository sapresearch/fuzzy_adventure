from programmer import *
from team import *
from bug import *
from software import *
from message import *
import MySQLdb
from configuration import *
import nltk

PROGRAMMERS = get_nb_programmers()
TEAMS = get_nb_teams()
BUGS = get_nb_bugs()
SOFTWARES = get_nb_softwares()
MESSAGES = get_nb_messages()


# Open database connection
db = MySQLdb.connect(host="localhost",user="root",passwd="",db="batcave")

# Drop table if it already exist using execute() method.
db.query("DROP TABLE IF EXISTS programmers")
sql = """CREATE TABLE programmers (\
	ID INT NOT NULL, \
	FIRST_NAME CHAR(30), \
	LAST_NAME  CHAR(30), \
	TEAM_ID INT, \
	PRIMARY KEY (ID), \
	FOREIGN KEY (TEAM_ID) REFERENCES teams(ID))"""
db.query(sql)


db.query("DROP TABLE IF EXISTS teams")
sql = """CREATE TABLE teams ( \
	ID INT NOT NULL, \
	MANAGER CHAR(30), \
	SUPER_ID INT, \
	PRIMARY KEY (ID))"""
db.query(sql)

db.query("DROP TABLE IF EXISTS bugs")
sql = """CREATE TABLE bugs (\
	ID INT NOT NULL,\
	START_DATE date, \
	CLOSE_DATE date, \
	CUSTOMER_ID int, \
	SOFTWARE_ID INT, \
	PROGRAMMER_ID int, \
	DESCRIPTION text, \
	PRIMARY KEY (ID), \
	FOREIGN KEY (SOFTWARE_ID) REFERENCES softwares(ID), \
	FOREIGN KEY (PROGRAMMER_ID) REFERENCES programmers(ID))"""
db.query(sql)

db.query("DROP TABLE IF EXISTS softwares")
sql = """CREATE TABLE softwares ( \
	ID varchar(255) NOT NULL, \
	TEAM_ID INT, \
	PRIMARY KEY (ID), \
	FOREIGN KEY (TEAM_ID) REFERENCES teams(ID))"""
db.query(sql)

db.query("DROP TABLE IF EXISTS messages")
sql = """CREATE TABLE messages (
	ID INT NOT NULL, \
	MESSAGE text, \
	PROGRAMMER_ID int, \
	CUSTOMER_ID int, \
	BUG_ID int, \
	REPLY_ID int, \
	PRIMARY KEY (ID), \
	FOREIGN KEY (PROGRAMMER_ID) REFERENCES programmers(ID), \
	FOREIGN KEY (BUG_ID) REFERENCES bugs(ID))"""
db.query(sql)

def fill_programmers():
	for i in range(0, PROGRAMMERS):
		programmer = RandomProgrammer()
		# Prepare SQL query to INSERT a record into the database.
		sql = """INSERT INTO programmers (ID, FIRST_NAME,LAST_NAME, TEAM_ID) VALUES (%d, '%s', '%s', %d)""" \
		% (programmer.id, programmer.first_name, programmer.last_name, programmer.team_id)
		db.query(sql)

		
def fill_teams():
	for i in range(0,TEAMS):
		team = RandomTeam()
		# Prepare SQL query to INSERT a record into the database.
		sql = """INSERT INTO teams (ID, MANAGER, SUPER_ID) VALUES (%d, '%s', %d)""" \
		% (team.id, team.manager, team.super_team_id)
		db.query(sql)
	
def fill_bugs():
	for i in range(0, BUGS):
		bug = RandomBug()
		sql = """INSERT INTO bugs (ID, START_DATE, CLOSE_DATE, CUSTOMER_ID, SOFTWARE_ID, PROGRAMMER_ID, DESCRIPTION) \
		VALUES (%d, '%s', '%s', %d, %d, %d, '%s')""" \
		% (bug.id, bug.start_date, bug.close_date, bug.customer_id, bug.software_id, bug.programmer_id, bug.description)
		db.query(sql)

def fill_softwares():
	all_software = []
	for i in range(0,SOFTWARES):
		family = generate_software_family(i)
		all_software += family
		responsible_team = random.randint(1, TEAMS)
		for member in family:
			# Add what team_id is responsible for that software family
			member.team_id = responsible_team
			#print "Software id %-15s | Team id %-d" % (member.id, member.team_id)
			# Prepare SQL query to INSERT a record into the database.
			sql = """INSERT INTO softwares (ID, TEAM_ID) VALUES ('%s', %d)""" \
			% (member.id, member.team_id)
			db.query(sql)

	
def fill_messages():
	for i in range(0, MESSAGES):
		message = RandomMessage()
		# Prepare SQL query to INSERT a record into the database.
		sql = """INSERT INTO messages (ID, MESSAGE, PROGRAMMER_ID, CUSTOMER_ID, BUG_ID, REPLY_ID) \
		VALUES (%d, '%s', %d, %d, %d, %d)""" \
		% (message.id, str(MySQLdb.escape_string(str(message.text_body))), message.programmer_to, message.customer_from, message.bug_id, message.reply_id)
		#print "%3d, %s, %3d, %3d, %3d, %3d" % (message.id, MySQLdb.espace_string(message.text_body), message.programmer_to, message.customer_from, message.bug_id, message.reply_id)
		db.query(sql)
	
fill_programmers()
fill_teams()
fill_bugs()
fill_softwares()
fill_messages()

db.query("""SELECT * FROM programmers""")
results = db.store_result().fetch_row(0)
for i in range (0, len(results), 30):
	print "Id %-3d | Name %-25s | Team id %-2d" % (results[i][0], results[i][1] + ' ' + results[i][2], results[i][3])

db.query("""SELECT * FROM teams""")
results = db.store_result().fetch_row(0)
for i in range (0, len(results)):
	print "Team id %2d | Manager %s | Super team id %d" % (results[i][0], results[i][1], results[i][2])	

db.query("""SELECT * FROM bugs""")
results = db.store_result().fetch_row(0)
for i in range(0,len(results), len(results) / 10):
	print "ID %-3d | Start %s | Close %-10s | Customer id %-2d | Software id %-2d | Programmer id %-2d" \
	% (results[i][0], results[i][1], results[i][2], results[i][3], results[i][4], results[i][5])

db.query("""SELECT * FROM softwares""")
results = db.store_result().fetch_row(0)
for i in range (0, len(results), len(results) / 10):
	print "Software ID %15s | Team id %-3d" % (results[i][0], results[i][1])	

db.query("""SELECT * FROM messages""")
results = db.store_result().fetch_row(0)
for i in range (0, len(results), len(results) / 10):
	print "Id %-3d | Message %s\n\tProgrammer id %-3d | Customer id %-3d | Bug id %-3d | Reply id %-3d" % \
	(results[i][0], results[i][1], results[i][2], results[i][3], results[i][4], results[i][5])	
	
db.close()
