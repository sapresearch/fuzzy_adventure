import pandas as pd
from pandas import DataFrame, Series
from numpy import random


firstNameMale = open('names/firstNameMale.txt', 'r').readlines()
firstNameFemale = open('names/firstNameFemale.txt', 'r').readlines()
surname = open('names/surname.txt', 'r').readlines()
firstName = firstNameMale + firstNameFemale


def generate_random_name(serie):
    name = firstName[random.random_integers(len(firstName)-1)].strip() + ' ' + surname[random.random_integers(len(surname) - 1)].strip()
    return name

print ("Processing programmers")
prog = pd.read_csv('originals/programmers.csv')
prog['FULL_NAME'] = ''
prog.FULL_NAME = prog.FULL_NAME.apply(generate_random_name)
prog.FULL_NAME[prog.NAME.isnull()] = ''

prog_with_name = open('to_import/programmers.csv','w')
prog.to_csv(prog_with_name, index = False)



def generate_random_mpt(serie):
    return random.gamma(2, 0.2)
print ("Processing transactions")
tran = pd.read_csv('originals/transactions.csv')
tran['MPT'] = 0
tran.MPT = tran.MPT.apply(generate_random_mpt)

tran_enhanced = open('to_import/transactions.csv','w')
tran.to_csv(tran_enhanced, index = False)


print ("Creating touched relations between transactions and programmers")
df = tran.merge(prog, left_on='PROGRAMMER_ID',right_on='ID', sort=False)
df.sort(columns=['ID_x'], inplace=True)

df = df[df.FULL_NAME != '']

touched = []
programmers_id = prog[prog.NAME.notnull()].ID.values
for i in df[['ID_x', 'ID_y']].values:
    num_touched = random.random_integers(10)
    touched.append({'TRANSACTION_ID': i[0], 'PROGRAMMER_ID':i[1]})
    for t in range(num_touched - 1):
        touched.append({'TRANSACTION_ID': i[0], 'PROGRAMMER_ID':programmers_id[random.random_integers(len(programmers_id)-1)]})

touched_df = DataFrame(touched)
touched_df.to_csv('to_import/touched.csv')