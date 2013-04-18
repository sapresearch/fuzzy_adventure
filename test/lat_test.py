from fuzzy_adventure.test import load_data
import question_type
import time

training = 'lat_data.txt'
testing = 'test_data.txt'

train_questions, _, lex_types = load_data.load_data(training)
test_questions, _, answer_types = load_data.load_data(testing)
total = len(test_questions)

start = time.time()
correct = 0.

model, word_vectors = question_type.train(train_questions, lex_types)
for i,q in enumerate(test_questions):
	answer = answer_types[i]
	prediction = question_type.classify(q, model, word_vectors)
	correct = correct+1 if answer == prediction else correct
duration = time.time() - start

accuracy = correct/total
print "Accuracy: " + str(accuracy)
