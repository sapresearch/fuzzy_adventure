import re
import json
# from fuzzy_adventure.query_decomposition.nlp_system import nlp_nlidb


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
    f.close()
    return questions, answers, lex_types

def load_questions(file_name):
    f = open(file_name, 'r')
    json_object = json.load(f)

    f.close()
    types = []
    questions = []

    for line in json_object:
        question = str(line['question'])
        # allWords, _, _, _, _, _, _ = nlp_nlidb.nlp_nlidb(question)
        # streamlined_q = ' '.join(allWords).lower()
        # if streamlined_q == '':
        #     print "Not processed:", question
        #     continue
        questions.append(question)
        types.append(str(line['type']))

    return questions, types

