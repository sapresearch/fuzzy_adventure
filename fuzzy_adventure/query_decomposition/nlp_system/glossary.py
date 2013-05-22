
from nltk import WordNetLemmatizer as WN_Lemmatizer
from nltk.stem import PorterStemmer as PStemmer
from fuzzy_adventure.external import en
import string
import os
from os import path, access, R_OK
from fuzzy_adventure.debug import debug

PATH=os.environ['FUZZY_ADVENTURE'] + "/context_based_data/glossary_processed.txt"


# Reads the words in the glossary text file and saves each synonym as a key and each label as 
# a value. Then seperates the phrases base on their word counts and save them in the relevant glossary.
'''To create the glossary for the first time:'''
def createGlossary():
	# sys.path.append('/home/I837185/git/fuzzy_adventure/Context-based Data/')
	glossary = open(os.environ['FUZZY_ADVENTURE'] + "/context_based_data/glossary.txt", 'r') 
	# open("../../context_based_data/glossary.txt", 'r')
	glossary_processed = open(os.environ['FUZZY_ADVENTURE'] + "/context_based_data/glossary_processed.txt", 'a')
	# open("../../context_based_data/glossary_processed.txt", 'a')
	text = glossary.readlines()
	# values = []
	glossary_one_word = dict()
	glossary_two_words = dict()
	glossary_three_words = dict()
	glossary_four_words = dict()
	for line in text: 
		line.strip()
		index = line.find('=')
		if index != -1:
		 	value = line[:index].strip()
		 	# print '1', value
			# if en.is_noun(value):
				# value = en.noun.singular(value)
			# value = WN_Lemmatizer().lemmatize(value)
			# print '2',value
			# elif en.is_verb(value):
				# value = en.verb.infinitive(value)
			value = PStemmer().stem(value)
			# print '2', value
		 	# print 'value:' , value
			start = line.find('[')
			end = line.find (']')
			valuesLines= line[index + 3: end ]
			vals = valuesLines.strip().lower()
			list_of_labels = vals.split(',')

			for label in list_of_labels:
				# print 'test label:',label
				words = label.split()
				wordCount = len(words)
				for i in range(wordCount):
					if wordCount == 1:
						label = label.lower()
						# if en.is_noun(label):
						# 	# label = en.noun.singular(label)
						# 	label = WN_Lemmatizer().lemmatize(label)
						# elif en.is_verb(label):
						# 	# label = en.verb.infinitive(label)
						label = PStemmer().stem(label)
						glossary_one_word[label.strip()] = value.lower()
					elif wordCount == 2:
						l=''
						for w in words:
							# print 'word', w
							w = w.lower()
							# if en.is_noun(w):
							# 	# w = en.noun.singular(w)
							# 	w = WN_Lemmatizer().lemmatize(w)
							# elif en.is_verb(w):
							# 	# w = en.verb.infinitive(w)
							w = PStemmer().stem(w)
							l= l + ' ' + w
							# print 'changed:', w
						glossary_two_words[l.strip()] = value.lower()

					elif wordCount == 3:
						l=''
						for w in words:
							# print 'word', w
							w = w.lower()
							# if en.is_noun(w):
							# 	# w = en.noun.singular(w)
							# 	w = WN_Lemmatizer().lemmatize(w)
							# elif en.is_verb(w):
							# 	# w = en.verb.infinitive(w)
							w = PStemmer().stem(w)
							l= l + ' ' + w
							# print 'changed:', w
						glossary_three_words[l.strip()] = value.lower()
					elif wordCount == 4:
						l=''
						for w in words:
							w1 = w.lower()
							# if en.is_noun(w1):
							# 	w1 = WN_Lemmatizer().lemmatize(w1)
							# 	# w1 = en.noun.singular(w1)
							# elif en.is_verb(w1):
							w1 = PStemmer().stem(w1)
								# w1 = en.verb.infinitive(w1)
							l= l + ' ' + w1
						glossary_four_words[l.strip()] = value.lower()
	glossary_processed.write ( str(glossary_one_word))
	glossary_processed.write ( str(glossary_two_words))
	glossary_processed.write ( str(glossary_three_words))
	glossary_processed.write ( str(glossary_four_words))
	# print  'one words:', glossary_one_word
	# print  'two words:', glossary_two_words
	# print  'three words:',glossary_three_words
	# print  'four words:',glossary_four_words
	return glossary_one_word, glossary_two_words, glossary_three_words, glossary_four_words

'''To read the existing glossary'''
def readGlossary():

	glossary_one_word = dict()
	glossary_two_words = dict()
	glossary_three_words = dict()
	glossary_four_words = dict()

	glossary = open(PATH,'r')

	text = glossary.read()
	i=0

	while i<=3:
		start = findnth(text, '{', i)
		end = findnth(text, '}', i) + 1
		temp_glossary = text[start:end]
		gl = eval(temp_glossary)
		# print gl
		if i==0:
			glossary_one_word = gl
		if i==1:
			glossary_two_words = gl
		if i==2:
			glossary_three_words = gl
		if i==3:
			glossary_four_words = gl
		i = i+1

	return glossary_one_word, glossary_two_words, glossary_three_words, glossary_four_words

def findnth(text, val, n):
    parts= text.split(val, n+1)
    if len(parts)<=n+1:
        return -1
    return len(text)-len(parts[-1])-len(val)
	
def checkGlossary(question):
	#check the words
	glossaryMatches = []
	remove_list = []


	if type(question) is list:
		words = question
	elif type(question) is not list:
		q_noPunc = question.translate(string.maketrans("",""), string.punctuation)
		words = q_noPunc.split(" ")


	for i in range(len(words)):
		words[i] = words[i].lower()
		# if en.is_noun(words[i]):
		# 	words[i] = en.noun.singular(words[i])
		# elif en.is_verb(words[i]):
		# 	words[i] = en.verb.infinitive(words[i])
		words[i] = PStemmer().stem(words[i])

	if path.isfile(PATH) and access(PATH, R_OK):
	    glossary_one_word, glossary_two_words, glossary_three_words, glossary_four_words = readGlossary()
	else:
		glossary_one_word, glossary_two_words, glossary_three_words, glossary_four_words = createGlossary()

	'''check four words glossary'''
	phrase = ''
	for i in range(len(words)-3):
		phrase = ' '. join(words[i:i+4])
		if phrase in glossary_four_words:
			glossaryMatches.append(glossary_four_words[phrase])
			for w in words[i:i+4]:
				remove_list.append(w)
			words = [x for x in words if x not in phrase.split()]

	''''check three words glossary:'''
	phrase = ''
	for i in range(len(words)-2):
		phrase = ' '. join(words[i:i+3])
		if phrase in glossary_three_words:
			glossaryMatches.append(glossary_three_words[phrase])
			for w in words[i:i+3]:
				remove_list.append(w)
			words = [x for x in words if x not in phrase.split()]
	'''check two words glossary:'''
	phrase = ''
	for i in range(len(words)-1):
		phrase = ' '. join(words[i:i+2])
		if phrase in glossary_two_words:
			glossaryMatches.append(glossary_two_words[phrase])
			for w in words[i:i+2]:
				remove_list.append(w)
			words = [x for x in words if x not in phrase.split()]

	# #check one word glossary:
	# if type(question) is not list:

	# for k in question.split() :
	for k in words:
		k = k.rstrip()
		k = k.lstrip()
		if k.strip() in glossary_one_word:

			glossaryMatches.append(glossary_one_word[k])
			remove_list.append(k)

	# print remove_list
	return glossaryMatches, remove_list

def generalizedKeywords(question, keyWords):
	'''Two calls to the checkGlossary, once with the question and once with the keywords, to find all possible matches'''
	glossaryMatches1, remove_list1 = checkGlossary(question)
	glossaryMatches2, remove_list2 = checkGlossary(keyWords)

	glossaryMatches = glossaryMatches1+glossaryMatches2
	if len(glossaryMatches) != 0:
		statement = 'glossaryMatches = ' + str(glossaryMatches)
		debug.debug_statement(statement)
	remove_list = remove_list1 + remove_list2
	# print glossaryMatches
	keyWords = [x for x in keyWords if x not in remove_list]
	uniqueWords = list(set(keyWords + glossaryMatches))
# >>>>>>> 1fb6ded45ada99e511032183b2346e8fa99840f5
	return uniqueWords