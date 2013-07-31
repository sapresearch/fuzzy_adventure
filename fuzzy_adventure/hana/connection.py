#import pypyodbc as pdbc
import getpass
import sys

cnxn = None
def get_cursor():
    global cnxn
    retry = True
    tries = 1

    if cnxn is None or cnxn.connected == 0:
        while retry and tries <= 5:
            if not hasattr(get_cursor, "userName"):
                get_cursor.userName = raw_input('User: ')

            if not hasattr(get_cursor, "password"):
                get_cursor.password = getpass.getpass('Password: ')            

            try:
                pdbc = __import__('pypyodbc')
                usrName = str(get_cursor.userName)
                pwd = str(get_cursor.password)
                param = "DSN=hana;UID=%s;PWD=%s" % (usrName, pwd)
                cnxn = pdbc.connect(param)
                retry = False
            except pdbc.Error as err:
                print param
                print err.args
                print 'Username and/or Password are incorrect'
                delattr(get_cursor,"userName")
                delattr(get_cursor,"password")
            tries += 1

    return cnxn.cursor()
