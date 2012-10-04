import re

""" This is here because if it's in the question_test.py file, then there's a loop when
question_test requires fuzzy_adventure, which requires question_type, which requires question_test """
def load_data(file_name):
	questions, answers, lex_types = [], [], []
	f = file(file_name)
	for line in f.readlines():
		line = line.split("\t")
		lex_type = line.pop(-1)
		lex_type = re.sub("[\r\n]", '', lex_type)
		question = line.pop(0)
		answer = line

		lex_types.append(lex_type)
		questions.append(question)
		answers.append(answer)
	return questions, answers, lex_types

