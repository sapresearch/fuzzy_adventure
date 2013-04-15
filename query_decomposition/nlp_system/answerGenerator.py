''' Answer generator includes a list of rules that are manually entered by the user to improve the performance and find the answer'''

def answerGenerator(question, allWords):
#definitions:
	conditions, what = set(), set()


	if 'causes delay' in allWords:
		allWords.append('component')
		conditions.add('causes delay')

	if 'backlog' in allWords:
		allWords.append('transaction')
		allWords.append('component')
		what.add('transaction')
	if 'messages' in allWords:
		allWords.append('messages')
		allWords.append('transaction')
		what.add('transaction')

	if 'solve' in allWords:
		allWords.append('transaction')
		conditions.add('solve')
		what.add('transaction')

	if 'most' in allWords or 'most' in question.split():
		# print question.split()
		conditions.add('Maximum value')
		what.add('transaction')

	if 'hiring date' in allWords:
		conditions.add('hiring date')
		what.add('transaction')
		what.add('employee')

	if 'MPT' in question.split():
		if 'average' in question.split():
			allWords.append('transaction')
			what.add('transaction')
			conditions.add('average')
		elif 'percent' in question.split():
			allWords.append('transaction')
			what.add('transaction')
			conditions.add('percent')
		elif 'most' in question.split():
			allWords.append('transaction')
			what.add('transaction')
			conditions.add('most')
	if 'escalated' in question.split() or 'escalated' in allWords:
		conditions.add('flag_escalated')
	if 'IRT' in question.split() or 'IRT' in allWords:
			allWords.append('IRT')
			what.add('transaction')



	if 'average' in question.split():
		conditions.add('average')

	if 'my' in question.split():
		#manager_ID = raw_input("what is your Employee ID?")
		manager_ID = '45'
		if manager_ID:
			conditions.add(str('manager_ID: '+ manager_ID))
		else: 
			conditions.add('manager_ID Was not provided by the manager!')

	if 'productive' in allWords:
		what.add('transaction')
		conditions.add('programmer')
		conditions.add('priority')
		#start_date = raw_input('Please enter the start date to calculate the productivity: ')
		start_date = '45'

		if start_date:
			what.add('transaction')
			conditions.add(start_date)
		else:
			conditions.add('Duration: Last 30 days')
		#end_date = raw_input ('Please enter the end date to calculate the productivity: ')
		end_date = '45'

		if end_date:
			what.add('transaction')
			conditions.add('end_date')

	if 'component' in allWords:
		what.add('component')

	if 'causes delay' in allWords:
		what.add('component')
		what.add('transaction')
		conditions.add('Maximum')
	
	if 'average' in allWords or 'average' in question.split():
		what.add('component')
		what.add('transaction')
		conditions.add('average')


	allWords = list(set(allWords))
	return allWords, conditions, what
