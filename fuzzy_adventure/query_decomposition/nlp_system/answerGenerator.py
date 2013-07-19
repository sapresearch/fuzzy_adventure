from nltk.stem import PorterStemmer as PStemmer
from components import *
import types
''' Answer generator includes a list of rules that are manually entered by the user to improve the performance and find the answer'''

# def checkRelation(allWords):
# 	if ('best' && 'employee') in allWords:
# 		return 'most effective'

def returnTime():
	conditions_temp = set()
	what_temp = set()
	# start_date = raw_input('Please enter the start date to do the calculations:')
	start_date = '45'
	end_date = '45'

	what_temp.add('transaction')
	conditions_temp.add(start_date)
	conditions_temp.add('end_date')
	conditions_temp.add('Duration: Last 30 days')
	# if start_date:
	# 	what_temp.add('transaction')
	# 	conditions_temp.add(start_date)
	# 	# end_date = raw_input ('Please enter the end date to calculate the productivity: ')
	# 	# # end_date = '45'

	# 	# # if PStemmer().stem(end_date):
	# 	# # 	what_temp.add('transaction')
	# 	# # 	conditions_temp.add('end_date')

	# 	if end_date:
	# 		what_temp.add('transaction')
	# 		conditions_temp.add('end_date')
	# else:
	# 	conditions_temp.add('Duration: Last 30 days')

	# # if PStemmer().stem(start_date):
	# # 	what_temp.add('transaction')
	# # 	conditions_temp.add(start_date)
	# # else:
	# # 	conditions.add('Duration: Last 30 days')

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
	conditions,what,conditions_temp,what_temp  =  set(),set(),set(),set()

	if 'causes delay' in allWords or 'causes delay' in question or stemmed('causes delay') in allWords or stemmed('causes delay') in question:
		allWords.append('component')
		conditions.add('causes delay')

	if stemmed('backlog') in allWords or stemmed('backlog') in question:
		allWords.append('transaction')
		allWords.append('component')
		what.add('transaction')

	if 'messages' in allWords or 'messages' in question or stemmed('messages') in allWords or stemmed('messages') in question:
		allWords.append('messages')
		allWords.append('transaction')
		what.add('transaction')

	if 'solve' in allWords or 'solve' in question or stemmed('solve') in allWords or stemmed('solve') in question:
		allWords.append('transaction')
		conditions.add('STATUS = closed')
		what.add('transaction')

	if 'most' in allWords or 'most' in question:
		conditions.add('Maximum value')
		what.add('transaction')

	if 'hiring date' in allWords or 'hiring date' in question or stemmed('hiring date') in allWords or stemmed('hiring date') in  question:
		conditions.add('hiring date')
		what.add('transaction')
		what.add('employee')

	if 'MPT' in allWords or 'MPT' in question:
		if 'percent' in allWords or 'percent' in question:
			allWords.append('transaction')
			what.add('transaction')
			conditions.add('percent')
		elif 'most' in allWords or 'most' in question:
			allWords.append('transaction')
			what.add('transaction')
			conditions.add('most')
	if 'escalated' in allWords or 'escalated' in question or stemmed('escalated') in allWords or stemmed('escalated')in  question:
		conditions.add('flag_escalated')
	if 'IRT' in allWords or 'IRT' in question:
			print 'de-escalated', 'yes'
			allWords.append('IRT')
			what.add('transaction')

	if 'average' in allWords or 'average' in question:
		conditions.add('average')
		allWords.append('transaction')
		what.add('transaction')
		what.add('component')

	if 'my' in allWords or 'my' in question:
		#manager_ID = raw_input("what is your Employee ID?")
		manager_ID = '45'
		if manager_ID:
			conditions.add(str('manager_ID: '+ manager_ID))
		else: 
			conditions.add('manager_ID Was not provided by the manager!')
	if 'support from my supervisor' in question:
		allWords.append('experienced')
		what.add('employee')

	if stemmed('productive') in allWords or stemmed('productive') in question:
		what.add('transaction')
		conditions.add('programmer')
		conditions.add('priority')
		start_date, end_date, conditions_temp,what_temp = returnTime()
		conditions.update(conditions_temp)
		what.update(what_temp)
		# start_date = '45'

	if 'closed' in allWords or 'closed' in question or stemmed('closed') in allWords or stemmed('closed') in question:
		what.add('transaction')
		if 'when' in allWords or 'when' in question:
			start_date, end_date, conditions_temp,what_temp = returnTime()
			conditions.update(conditions_temp)
			what.update(what_temp)
		if 'number' in allWords or 'number' in question:
			conditions.add('number of closed tickets')

	if 'high' in allWords or 'high' in question:
		what.add('transaction')
		conditions_temp = 'high priority'
		conditions.update(conditions_temp)

	if 'low' in allWords or 'low' in question:
		what.add('transaction')
		conditions_temp = 'low'
		conditions.update(conditions_temp)

	if 'medium' in allWords or 'medium' in question:
		what.add('transaction')
		conditions_temp = 'medium'
		conditions.update(conditions_temp)






	if stemmed('component') in allWords or stemmed('component') in  question:
		what.add('component')


	component_Names = get_components()
	component_Names_l = list(component_Names)
	# print component_Names_l
	# print type(component_Names_l)
	for c_n in component_Names_l:

		if c_n!=None:
			c_n_asc = c_n.encode('ascii','ignore')
			if c_n_asc in question:
				what.add('component')
				allWords.append(c_n_asc)




	allWords = list(set(allWords))
	return allWords, conditions, what
