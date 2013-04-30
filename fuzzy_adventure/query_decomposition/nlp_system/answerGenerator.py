from nltk.stem import PorterStemmer as PStemmer
''' Answer generator includes a list of rules that are manually entered by the user to improve the performance and find the answer'''

# def checkRelation(allWords):
# 	if ('best' && 'employee') in allWords:
# 		return 'most effective'

def returnTime():
	start_date = raw_input('Please enter the start date to do the calculations:')
	# start_date = '45'

	if PStemmer().stem(start_date):
		what_temp.add('transaction')
		conditions_temp.add(start_date)
	else:
		conditions.add('Duration: Last 30 days')
	end_date = raw_input ('Please enter the end date to calculate the productivity: ')
	# end_date = '45'

	if PStemmer().stem(end_date):
		what_temp.add('transaction')
		conditions_temp.add('end_date')

	return start_date, end_date, conditions_temp,what_temp

def stemmed(word):
	l = ''
	words = word.split()
	for w in words:
		w = w.lower()
		w = PStemmer().stem(w)
		l= l + ' ' + w
	return l



def answerGenerator(question, allWords):
#definitions:
	conditions, what = set(), set()


	if 'causes delay' or stemmed('causes delay') in [allWords,question]:
		allWords.append('component')
		conditions.add('causes delay')

	if stemmed('backlog') in [allWords,question]:
		allWords.append('transaction')
		allWords.append('component')
		what.add('transaction')

	if 'messages' or stemmed('messages') in [allWords,question]:
		allWords.append('messages')
		allWords.append('transaction')
		what.add('transaction')

	if 'solve' or stemmed('solve') in [allWords,question]:
		allWords.append('transaction')
		conditions.add('STATUS = closed')
		what.add('transaction')

	if stemmed('most') in [allWords,question]:
		# print question.split()
		conditions.add('Maximum value')
		what.add('transaction')

	if 'hiring date' or stemmed('hiring date') in [allWords,question]:
		conditions.add('hiring date')
		what.add('transaction')
		what.add('employee')

	if 'MPT' in [allWords,question]:
		if 'percent' in [allWords,question]:
			allWords.append('transaction')
			what.add('transaction')
			conditions.add('percent')
		elif 'most' in [allWords,question]:
			allWords.append('transaction')
			what.add('transaction')
			conditions.add('most')
	if 'escalated' or stemmed('escalated') in [allWords,question]:
		conditions.add('flag_escalated')
	if 'IRT' in [allWords,question]:
			allWords.append('IRT')
			what.add('transaction')



	if 'average' in [allWords,question]:
		conditions.add('average')
		allWords.append('transaction')
		what.add('transaction')
		what.add('component')

	if 'my' in [allWords,question]:
		#manager_ID = raw_input("what is your Employee ID?")
		manager_ID = '45'
		if manager_ID:
			conditions.add(str('manager_ID: '+ manager_ID))
		else: 
			conditions.add('manager_ID Was not provided by the manager!')

	if stemmed('productive') in [allWords,question]:
		what.add('transaction')
		conditions.add('programmer')
		conditions.add('priority')
		start_date, end_date, conditions_temp,what_temp = returnTime()
		conditions.add(conditions_temp)
		what.add(what_temp)
		# start_date = '45'

		# if start_date:
		# 	what.add('transaction')
		# 	conditions.add(start_date)
		# else:
		# 	conditions.add('Duration: Last 30 days')

		# end_date = '45'
		# if end_date:
		# 	what.add('transaction')
		# 	conditions.add('end_date')
	if 'closed' or stemmed('closed') in [allWords,question]:
		what.add('transaction')
		if 'when' in [allWords,question]:
			start_date, end_date, conditions_temp,what_temp = returnTime()
			conditions.add(conditions_temp)
			what.add(what_temp)
		if 'number' in [allWords,question]:
			conditions.add('number of closed tickets')



	if stemmed('component') in [allWords,question]:
		what.add('component')



	allWords = list(set(allWords))
	return allWords, conditions, what
