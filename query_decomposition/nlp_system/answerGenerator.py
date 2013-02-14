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

	if 'solve' in allWords:
		allWords.append('transaction')
		conditions.add('solve')
		what.add('transaction')

	if 'most' in allWords or question.split():
		# print question.split()
		conditions.add('Maximum value')
		what.add('transaction')

	if 'my' in question.split():
		manager_ID = raw_input("what is your Employee ID?")
		if manager_ID:
			conditions.add(str('manager_ID: '+ manager_ID))
		else: 
			conditions.add('manager_ID Was not provided by the manager!')

	if 'productive' in allWords:
		what.add('transaction')
		conditions.add('programmer')
		conditions.add('priority')
		start_date = raw_input('Please enter the start date to calculate the productivity: ')

		if start_date:
			what.add('transaction')
			conditions.add(start_date)
		else:
			conditions.add('Duration: Last 30 days')
		end_date = raw_input ('Please enter the end date to calculate the productivity: ')

		if end_date:
			what.add('transaction')
			conditions.add('end_date')

	if 'component' in allWords:
		what.add('component')

	if 'causes delay' in allWords:
		what.add('component')
		what.add('transaction')
		conditions.add('Maximum')

	allWords = list(set(allWords))
	return allWords, conditions, what
