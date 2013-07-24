import connexion
import sys
import pickle
import datetime

cur = None

def create_tables():
    cur = connexion.get_cursor(args[1],args[2])

    cur.execute("""CREATE TABLE transactions(
            trans_number      VARCHAR(50), 
            programmer_id     INT, 
            start_date        DATETIME, 
            end_date          DATETIME,
            status            VARCHAR(30), 
            priority          VARCHAR(20),
            contract_priority VARCHAR(10),
            product           VARCHAR(30),
            os                VARCHAR(15),
            system_type       CHAR,
            attribute         VARCHAR(10),
            solving_level     VARCHAR(10),
            flag_24h          CHAR,
            component_id      INT) """)

    cur.execute("""CREATE TABLE programmers( 
            name VARCHAR(80))""")
            
    cur.execute("""CREATE TABLE components(
            name VARCHAR(30))""")


def import_transactions():
    file = open('transactions', 'rb')
    t = pickle.load(file)
    file.close()

    print "Importing transactions"
    for trans in t:
        try:
            cur.execute("""insert into transactions values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (trans[1], int(trans[2]), trans[3], trans[4], trans[5], trans[6], trans[7], trans[8], trans[9], trans[10], trans[11], trans[12], trans[13], int(trans[14])))
        except:
            print "Failed transaction"
            print trans


def import_programmers():
    file = open('programmers', 'rb')
    p = pickle.load(file)
    file.close()

    print "Importing programmers"
    for programmer in p:
        try:
            cur.execute("""insert into programmers values(?)""", (programmer[1]))
        except:
            print "Failed programmers"
            print programmer


def import_components():
    file = open('components', 'rb')
    c = pickle.load(file)
    file.close()

    print "Importing components"
    for component in c:
        try: 
            cur.execute("""insert into components values(?)""", (component[1]))
        except:
            print "Failed transaction"
            print trans



if __name__ == '__main__':
    args = sys.argv
    if len(args) != 3:
        sys.exit("You must provide the username and password on the command line.")

    create_tables()
    import_transactions()
    import_programmers()
    import_components()

