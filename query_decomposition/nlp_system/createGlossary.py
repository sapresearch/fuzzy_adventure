import sys
# from nltk import WordNetLemmatizer as WN_Lemmatizer
# from nltk.stem import PorterStemmer as PStemmer
import en
# Reads the words in the glossary text file and saves each synonym as a key and each label as 
# a value. The seperates the phrases base on their word counts and save them in the relevant glossary.
def createGlossary():
	# sys.path.append('/home/I837185/git/fuzzy_adventure/Context-based Data/')
	glossary = open('glossary.txt', 'r')
	glossary_processed = open('glossary_processed.txt', 'a')
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
			start = line.find('[')
			end = line.find (']')
			valuesLines= line[index + 3: end ]
			vals = valuesLines.strip().lower()
			list_of_labels = vals.split(',')

			for label in list_of_labels:
				words = label.split()
				wordCount = len(words)
				for i in range(wordCount):
					if wordCount == 1:
						label = label.lower()
						if en.is_noun(label):
							w = en.noun.singular(w)
						elif en.is_verb(label):
							w = en.verb.infinitive(w)
						glossary_one_word[label.strip()] = value.lower()
					elif wordCount == 2:
						l=''
						for w in words:
							# print 'word', w
							w = w.lower()
							if en.is_noun(w):
								w = en.noun.singular(w)
							# 	w = WN_Lemmatizer().lemmatize(w)
							elif en.is_verb(w):
								w = en.verb.infinitive(w)
							# 	w = PStemmer().stem(w)
							l= l + ' ' + w
							# print 'changed:', w
						glossary_two_words[l.strip()] = value.lower()

					elif wordCount == 3:
						l=''
						for w in words:
							# print 'word', w
							w = w.lower()
							if en.is_noun(w):
								w = en.noun.singular(w)
							# 	w = WN_Lemmatizer().lemmatize(w)
							elif en.is_verb(w):
								w = en.verb.infinitive(w)
							# 	w = PStemmer().stem(w)
							l= l + ' ' + w
							# print 'changed:', w
						glossary_three_words[l.strip()] = value.lower()
					elif wordCount == 4:
						l=''
						for w in words:
							w1 = w.lower()
							if en.is_noun(w1):
								w1 = en.noun.singular(w1)
							elif en.is_verb(w1):
								w1 = en.verb.infinitive(w1)
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
