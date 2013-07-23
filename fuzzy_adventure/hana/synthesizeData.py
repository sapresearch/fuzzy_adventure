import connection
import numpy as np
from numpy import random

cur = connection.get_cursor()
#cur.execute("""ALTER TABLE PROGRAMMERS ADD (FULL_NAME nvarchar(50))""")
#cur.execute("""ALTER TABLE PROGRAMMERS ALTER (FULL_NAME nvarchar(50))""")
cur.execute("""SELECT ID FROM PROGRAMMERS WHERE NAME IS NOT NULL""")
ids = [i[0] for i in cur.fetchall()]

firstNameMale = open('firstNameMale.txt', 'r').readlines()
firstNameFemale = open('firstNameFemale.txt', 'r').readlines()
surname = open('surname.txt', 'r').readlines()
firstName = firstNameMale + firstNameFemale

names = []
for i in ids:
    name = firstName[random.random_integers(len(firstName)-1)].strip() + ' ' + surname[random.random_integers(len(surname) - 1)].strip()
    names.append((str(name), i))

cur.executemany("""UPDATE PROGRAMMERS SET full_name=? WHERE id=?""", names)
cur.commit()


query = """CREATE ROW TABLE "TOUCHED" ( "ID" INT CS_INT NOT NULL,
     "TRANSACTION_ID" INT CS_INT NOT NULL,
     "PROGRAMMER_ID" INT CS_INT NOT NULL,
     PRIMARY KEY ( "ID" ) ) """

cur.execute(query)
cur.execute("""SELECT TRANSACTIONS.ID, PROGRAMMER_ID FROM TRANSACTIONS INNER JOIN PROGRAMMERS ON TRANSACTIONS.PROGRAMMER_ID = PROGRAMMERS.ID WHERE PROGRAMMERS.NAME IS NOT NULL""")
ids = [(i[0], i[1]) for i in cur.fetchall()]
cur.execute("""SELECT ID FROM PROGRAMMERS WHERE NAME IS NOT NULL""")
programmers_id = [i[0] for i in cur.fetchall()]


num = 0
touched = []
for i in ids:
    num_touched = random.random_integers(10)
    touched.append((num, i[0], i[1]))
    num += 1
    for t in range(num_touched - 1):
        touched.append((num, i[0], programmers_id[random.random_integers(len(programmers_id)-1)]))
        num += 1

cur.executemany("""INSERT INTO TOUCHED (ID, TRANSACTION_ID, PROGRAMMER_ID) VALUES (?,?,?)""", touched)
cur.commit()





cur.execute("""ALTER TABLE TRANSACTIONS ADD (MPT DECIMAL(3,2))""")
MPT = []
for i in ids:
    trans_id = i[0]
    MPT.append((random.gamma(2, 0.2), trand_id))

cur.executemany("""INSERT INTO TRANSACTIONS (MPT) VALUES (?) WHERE ID = ?""", MPT)
cur.commit()


tran.merge(self, right, how='inner', on=None, left_on=None, right_on=None, left_index=False, right_index=False, sort=False, suffixes=('_x', '_y'), copy=True)


