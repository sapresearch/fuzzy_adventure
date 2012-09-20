import sys
sys.path.append("../")
import fuzzy_adventure
import re
import time

def test(questions, answers, lex_types):
    correct_answers = 0.0
    correct_types = 0.0

    start = time.time()
    for q in questions:
        index = questions.index(q)
        real_answers = answers[index]
        lex_type = lex_types[index]
        predicted_answer, predicted_lex_type, _, _, _, _, _, _ = fuzzy_adventure.ask_question(q)

        print q
        if predicted_lex_type == lex_type:
					correct_types += 1
					print "Right! " + predicted_lex_type

        if predicted_answer in real_answers:
            correct_answers += 1
            print "CORRECT:" + predicted_answer + " in " + str(real_answers)
        else:
            print "Incorrect:" + predicted_answer + " not in " + str(real_answers)
        print "\n"
    duration = time.time() - start

    avg_time = duration / len(questions)
    answer_accuracy = correct_answers / len(questions) * 100.0
    type_accuracy = correct_types / len(questions) * 100.0
    answer_accuracy, type_accuracy, avg_time = round(answer_accuracy, 1), round(type_accuracy, 1), round(avg_time, 3)
    return answer_accuracy, type_accuracy, avg_time

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

questions, answers, lex_types = load_data('test_data.txt')
print test(questions, answers, lex_types)
