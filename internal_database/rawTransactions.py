import numpy as np
from datetime import datetime
from transactionFields import *


def import_transactions_from_file(file_name):
	"""
	Import transactions from a file. Every transaction will be a dictionnary(hash) {header: value}
	Return an array of dictionnaries(hashes) of all the transactions easily parsable.
	Every feature of a transaction in the array can be searched by the header.
	"""
	lines = load_file(file_name).readlines()
	if lines is None:
		return None
	
	# Fourth row contains the headers
	headers = splitColumns(lines[3])
	transactions = []
	transactions.append(cleanColumns(headers))
	for line in lines:
		splitted_line = splitColumns(line)

		if len(splitted_line) < len(headers):
			continue

		cleanColumns(splitted_line)

		# Sometimes the file can contain the headers in the middle of the file
		# Skip that line if that happens
		if splitted_line == headers:
			continue
		transactions.append(splitted_line)
		
	return buildTransactions(transactions)
	

def load_file(file_name):
	"""
	Simply loads and returns the file with the specified file name.
	"""
	try:
		file = open(file_name,"r")
		return file
	except IOError:
		print "Could not open the file", file_name

		
def splitColumns(line):
	"""
	Splits a line in column, based on the separator '|'. Each items are then stripped.
	"""
	columns = np.array(line.split('|'))
	columns = map(lambda x: x.strip(), columns)
	return columns
	
	
def cleanColumns(line):
	"""
	Some hardcoding for cleaning the columns. Some of the them are useless (first, second and last).
	Use this method only if the line has been split by columns before.
	"""
	line.pop(0)
	line.pop(0)
	line.pop()
	return line

	
def buildTransactions(transactions):
	"""
	Take in all the transactions, each previously splitted by columns, and return an
	array of dictionnaries(hashes). Those dictionnaries are the individual transactions with
	{header: value}
	"""
	# First row contains the headers
	headers = transactions[0]
	transactionsList = []
	for i in range(1, len(transactions)):
		transactionHash = {}
		for j in range(len(headers)):
			header = headers[j]
			item = transactions[i][j]
			transactionHash[header] = item
			
		transactionsList.append(transactionHash)
	return transactionsList
	
