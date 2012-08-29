from nltk.corpus import wordnet
import re

def lexical_answer_type(tree):
	match = re.search('ROOT \((\w*)', tree)
	result = match.group(1)
	question_type = ''
	if result == 'SQ':
		question_type = 'boolean'
	elif result == 'SBARQ':
		if re.match('.*[Ww]here', tree):
			question_type = 'location'
		elif re.match('.*[Ww]hen', tree):
			question_type = 'time'
		elif re.match('.*[Ww]ho', tree):
			question_type = 'person'
		else:
			question_type = 'unknown'
	else:
		question_type = 'unknown'
	return question_type

#print wordnet.synsets('dog')
tree = "(ROOT (SQ [82.586] (VBP [1.048] Do) (NP [14.749] (NNS [11.249] tigers)) (VP [62.572] (VB [6.877] live) (PP [16.231] (IN [1.552] in) (NP [14.006] (NNP [11.532] Sumuatra))) (SBAR [33.579] (IN [3.161] while) (S [30.091] (NP [11.656] (DT [0.650] the) (NN [8.843] weather)) (VP [18.103] (VBZ [0.144] is) (ADJP [13.233] (JJ [12.511] rainy)))))) (. [0.013] ?)))"
#tree = "(ROOT (SBARQ [58.275] (WHADVP [4.738] (WRB [4.673] Where)) (SQ [52.073] (VBP [0.435] do) (NP [14.749] (NNS [11.249] tigers)) (VP [33.679] (VB [6.877] live) (NP [24.769] (NN [8.432] while) (NN [11.979] bathing)))) (. [0.004] ?)))"
print lexical_answer_type(tree)
