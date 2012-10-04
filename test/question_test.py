import sys
sys.path.append("/home/I829287/fuzzy_adventure")
import fuzzy_adventure
import load_data
import re
import time


def test(questions, answers, lex_types):
    #create/open file for writing
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
        predicted_answer, confidence, predicted_lex_type, _, tree, _, _  = fuzzy_adventure.ask_question(q)

        # Count the total positives for LAT and answers
        if predicted_answer != "I don't understand the question" and predicted_answer != "I don't know":
            total_positives += 1.0
        if "I don't know" in real_answers and predicted_answer != "I don't understand the question":
            total_positives += 1.0
        if predicted_lex_type != "unknown":
            total_type_positives += 1.0

        # Count hte total correct answers and LAT
        fo.write("Confidence: " + str(confidence) + "\n" + q + "\nTree: " + str(tree))
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

    #calculate results
    avg_time = duration / len(questions)
    answer_recall = correct_answers / len(questions)
    type_recall = correct_types / len(questions)
    precision = correct_answers/total_positives
    lex_precision = correct_types/total_type_positives
    f1_score = 2. * (answer_recall * precision)/(answer_recall + precision)

    metrics = [f1_score, answer_recall, precision, type_recall, lex_precision, avg_time]
    rounded = []
    for m in metrics:
        rounded.append(round(m, 3))

    #write results to file
    fo.write("[F1 Score, Recall, Precision, Recall(type), Precision(type), Avg Time] = " + str(rounded))
    fo.close

    return rounded


questions, answers, lex_types = load_data.load_data('test_data.txt')
print test(questions, answers, lex_types)
