import pyodbc
cnxn = None
def get_cursor(userName, password):
    cnxn = pyodbc.connect('DSN=hana;UID=%s;PWD=%s' % (str(userName), str(password)))
    return cnxn.cursor()

