import sys
sys.path.append("/home/I829287/fuzzy_adventure/query_decomposition")
import load_data
import question_type
import time

path = 'test_data.txt'
questions, _, lex_types = load_data.load_data(path)
total = len(questions)

start = time.time()
correct = 0.
for x in range(2):
	train = (x+1) % 2
	test = x % 2

	train_questions = questions[train::2]
	train_lex_types = lex_types[train::2]
	test_questions = questions[test::2]
	test_lex_types = lex_types[test::2]
	model, word_vectors = question_type.train(train_questions, train_lex_types)

	for i,q in enumerate(test_questions):
		answer = test_lex_types[i]
		lexical_type = question_type.classify(q, model, word_vectors)
		correct = correct+1 if answer == lexical_type else correct
duration = time.time() - start

accuracy = correct/total
print "Accuracy: " + str(accuracy)
