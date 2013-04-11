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

rs = stmt.executeQuery("SELECT COUNT(*) FROM TRANSACTIONS")
rs.next() # rs (ResultSet) is set before the first line. Need to call next in order to point on the first
print rs.getInt(1) # Result is an int with one column only. Columns start at 1.



