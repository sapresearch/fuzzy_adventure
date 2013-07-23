import pypyodbc as pdbc
import getpass
cnxn = None
def get_cursor():
    if not hasattr(get_cursor, "userName"):
        get_cursor.userName = raw_input('User: ')
    if not hasattr(get_cursor, "password"):
        get_cursor.password = getpass.getpass('Password: ')

    if not hasattr(get_cursor, "cnxn"):
        c = "DSN=hana;UID=%s;PWD=%s" % (str(get_cursor.userName), str(get_cursor.password))
        get_cursor.cnxn = pdbc.connect(c)

    return get_cursor.cnxn.cursor()
