import pypyodbc as pdbc
import getpass
import sys

def get_cursor():
    retry = True
    tries = 1
    while retry and tries <= 5:
        if not hasattr(get_cursor, "userName"):
            get_cursor.userName = raw_input('User: ')
        if not hasattr(get_cursor, "password"):
            get_cursor.password = getpass.getpass('Password: ')

        if not hasattr(get_cursor, "cnxn"):
            try:
                c = "DSN=hana;UID=%s;PWD=%s" % (str(get_cursor.userName), str(get_cursor.password))
                get_cursor.cnxn = pdbc.connect(c)
                retry = False
            except pdbc.Error as err:
                print 'Username and/or Password are incorrect'
                delattr(get_cursor,"userName")
                delattr(get_cursor,"password")
        tries += 1

    if not hasattr(get_cursor,"cnxn"): 
        sys.exit('You failed 5 times to enter valid credentials. System exit.')

    return get_cursor.cnxn.cursor()
