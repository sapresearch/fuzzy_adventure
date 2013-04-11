import os
project_path = os.environ['FUZZY_ADVENTURE']
import sys
sys.path.append(project_path + '/hana/ngdbc.jar')
from com.sap.db.jdbc import Driver
from java.util import Properties
from java.sql import Connection
from java.sql import Statement


def get_statement():
    if not hasattr(get_statement, "userName"):
        get_statement.userName = raw_input('User: ')
    if not hasattr(get_statement, "password"):
        get_statement.password = raw_input('Password: ')

    if not hasattr(get_statement, "stmt"):
        d = Driver()
        props = Properties()
        props.setProperty("user", str(get_statement.userName)) # Put your HANA username
        props.setProperty("password", str(get_statement.password)) # Put your HANA password
        props.setProperty("driver_class_name", "HDBODBC")

        conn = d.connect("jdbc:sap://bostonresearch.bos.sap.corp:30115", props)
        stmt = conn.createStatement()

        get_statement.stmt = stmt

    return get_statement.stmt


stmt = get_statement()
stmt.execute("""DELETE FROM TOUCHED2""");
import csv
import time

print "Creating queries"
csv_file = open('to_import/touched.csv', 'rb')
reader = csv.reader(csv_file)
reader.next() #jump first line, which is header
for row in reader:
    value = (int(row[0]), int(row[2]), int(row[1]))
    query = """INSERT INTO TOUCHED2 (ID, TRANSACTION_ID, PROGRAMMER_ID) VALUES (%d, %d, %d))""" % value
    stmt.addBatch(query)

print "Executing all queries"
start = time.time()
stmt.executeBatch();
System.out.println("Duration: " + (time.time() - start))