from programmer import *
from team import *
from bug import *
from software import *
from message import *
import MySQLdb
from configuration import *

PROGRAMMERS = get_nb_programmers()
TEAMS = get_nb_teams()
BUGS = get_nb_bugs()
SOFTWARES = get_nb_softwares()
MESSAGES = get_nb_messages()


# Open database connection
db = MySQLdb.connect(host="localhost",user="root",passwd="",db="batcave")

# Drop table if it already exist using execute() method.
db.query("DROP TABLE IF EXISTS programmers")
sql = """CREATE TABLE programmers (ID INT, FIRST_NAME CHAR(30), LAST_NAME  CHAR(30), TEAM_ID INT)"""
db.query(sql)


db.query("DROP TABLE IF EXISTS teams")
sql = """CREATE TABLE teams (TEAM_ID INT, MANAGER CHAR(30), SUPER_TEAM_ID INT)"""
db.query(sql)

db.query("DROP TABLE IF EXISTS bugs")
sql = """CREATE TABLE bugs (START_DATE date, CLOSE_DATE date, CUSTOMER_ID int, SOFTWARE_ID INT, PROGRAMMER_ID int, DESCRIPTION varchar(255))"""
db.query(sql)

db.query("DROP TABLE IF EXISTS softwares")
sql = """CREATE TABLE softwares (SOFTWARE_ID INT, SUPER_SOFTWARE_ID INT)"""
db.query(sql)

db.query("DROP TABLE IF EXISTS messages")
sql = """CREATE TABLE messages (ID int, TEXT varchar(255), PROGRAMMER_ID int, CUSTOMER_ID int, BUG_ID int, REPLY_ID int)"""
db.query(sql)

def fill_programmers():
	for i in range(0, PROGRAMMERS):
		programmer = Programmer().get_new_programmer()
		# Prepare SQL query to INSERT a record into the database.
		sql = """INSERT INTO programmers (ID, FIRST_NAME,LAST_NAME, TEAM_ID) VALUES (%d, '%s', '%s', %d)""" \
		% (i + 1, programmer.first_name, programmer.last_name, programmer.team_id)
		db.query(sql)

		
def fill_teams():
	for i in range(0,TEAMS):
		team = Team().get_new_team()
		# Prepare SQL query to INSERT a record into the database.
		sql = """INSERT INTO teams (TEAM_ID, MANAGER, SUPER_TEAM_ID) VALUES (%d, '%s', %d)""" \
		% (i + 1, team.manager, team.super_team_id)
		db.query(sql)
	
def fill_bugs():
	for i in range(0, BUGS):
		bug = Bug().get_new_bug()
		sql = """INSERT INTO bugs (START_DATE, CLOSE_DATE, CUSTOMER_ID, SOFTWARE_ID, PROGRAMMER_ID, DESCRIPTION) \
		VALUES ('%s', '%s', %d, %d, %d, '%s')""" \
		% (bug.start_date, bug.close_date, bug.customer_id, bug.software_id, bug.programmer_id, bug.description)
		db.query(sql)

def fill_softwares():
	for i in range(0,SOFTWARES):
		software = Software().get_new_software()
		# Prepare SQL query to INSERT a record into the database.
		sql = """INSERT INTO softwares (SOFTWARE_ID, SUPER_SOFTWARE_ID) VALUES (%2d, %2d)""" \
		% (i + 1, software.super_software_id)
		db.query(sql)

def fill_messages():
	for i in range(0, MESSAGES):
		message = Message().get_new_message()
		# Prepare SQL query to INSERT a record into the database.
		sql = """INSERT INTO messages (ID, TEXT, PROGRAMMER_ID, CUSTOMER_ID, BUG_ID, REPLY_ID) \
		VALUES (%3d, '%s', %3d, %3d, %3d, %3d)""" \
		% (i + 1, message.text_body, message.programmer_to, message.customer_from, message.bug_id, message.reply_id)
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
for i in range(0,len(results),10):
	print "Start %s | Close %-10s | Customer id %-2d | Software id %-2d | Programmer id %-2d" \
	% (results[i][0], results[i][1], results[i][2], results[i][3], results[i][4])

db.query("""SELECT * FROM softwares""")
results = db.store_result().fetch_row(0)
for i in range (0, len(results), 5):
	print "Software id %-2d | Super software id %-d" % (results[i][0], results[i][1])	

db.query("""SELECT * FROM messages""")
results = db.store_result().fetch_row(0)
for i in range (0, len(results), 100):
	print "Id %-3d | Text %s\n\tProgrammer id %-3d | Customer id %-3d | Bug id %-3d | Reply id %-3d" % \
	(results[i][0], results[i][1], results[i][2], results[i][3], results[i][4], results[i][5])	
	
db.close()