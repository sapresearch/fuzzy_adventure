import pyodbc
cnxn = None
def getCursor(userName, password):
    cnxn = pyodbc.connect('DSN=hana;UID=%s;PWD=%s' % (str(userName), str(password)))
    return cnxn.cursor()

