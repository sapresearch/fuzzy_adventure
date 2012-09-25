import sys
sys.path.append("../")
import fuzzy_adventure
import re
import time


def test(questions, answers, lex_types):
    fo = open("output.txt", "wb")

    correct_answers = 0.0
    correct_types = 0.0
    total_positives = 0.0
    total_type_positives = 0.0

    start = time.time()
    for q in questions:
        index = questions.index(q)
        real_answers = answers[index]
        lex_type = lex_types[index]
        predicted_answer, predicted_lex_type, _, _, _, _, _, _ = fuzzy_adventure.ask_question(q)

        # Count the total positives for LAT and answers
        if predicted_answer != "I don't understand the question" and predicted_answer != "I don't know":
            total_positives += 1.0
        if predicted_lex_type != "unknown":
            total_type_positives += 1.0

        # Count hte total correct answers and LAT
        fo.write(q)
        if predicted_lex_type == lex_type:
            correct_types += 1
            fo.write("\nCorrect LAT: " + predicted_lex_type)
        else:
            fo.write("\nIncorrect LAT: " + predicted_lex_type + " does not equal " + lex_type)

        if predicted_answer in real_answers:
            correct_answers += 1
            fo.write("\nCORRECT answer:" + predicted_answer + " in " + str(real_answers))
        else:
            fo.write("\nIncorrect answer:" + predicted_answer + " not in " + str(real_answers))
        fo.write("\n\n")
    duration = time.time() - start

    avg_time = duration / len(questions)
    answer_recall = correct_answers / len(questions) * 100.0
    type_recall = correct_types / len(questions) * 100.0
    precision = correct_answers/total_positives * 100
    lex_precision = correct_types/total_type_positives * 100
    answer_recall, precision, type_recall, lex_precision, avg_time = round(answer_recall, 1), round(precision, 1), round(type_recall, 1), round(lex_precision, 1), round(avg_time, 3)

    output = [answer_recall, precision, type_recall, lex_precision, avg_time]
    fo.write("Recall, Precision, Recall(type), Precision(type), Avg Time) = " + str(output))
    fo.close

    return output

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
to_write = test(questions, answers, lex_types)
print to_write
fo.write("(Recall, Precision, Recall(type), Avg Time) = " + str(to_write))

#close opend file
fo.close()
