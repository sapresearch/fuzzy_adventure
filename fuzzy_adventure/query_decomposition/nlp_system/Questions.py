'''This code read the questions from questions.txt file and save them with their according keywords which is returned by the system in a text file called "processed_questions.txt"'''

import string
import os
from nlp_nlidb import keyWords_allQuestions

PATH_toRead=os.environ['FUZZY_ADVENTURE'] + "/context_based_data/questions.txt"
PATH_toWrite = os.environ['FUZZY_ADVENTURE'] + "/context_based_data/processed_questions.txt"

fileToRead = open(PATH_toRead,'r')
fileToWrite = open(PATH_toWrite, 'w')

question = fileToRead.readline()

while(question):
	# print question
	question = fileToRead.readline()
	if question.strip():
		question_no_punctuation = question.translate(string.maketrans("",""), string.punctuation)
		# fileToWrite.write(question_no_punctuation)
		fileToWrite.write(question)
		keyWords = keyWords_allQuestions(question_no_punctuation)
		fileToWrite.write('keyWords: ')
		fileToWrite.write(str(keyWords))
		fileToWrite.write('\r\n')
		fileToWrite.write("\r\n=========================================================================================================\r\n")







