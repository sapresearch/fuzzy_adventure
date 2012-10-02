import os
from os import system
import time
import re
import operator


def classify(sentence):
	input_path = "data/question_type/test.txt"
	output_path = "data/question_type/prob_test.out"
	labels_path = "data/question_type/labels.map"

	# Write input to be classfied
	f = open(input_path, "w")
	sentence = "\n".join(sentence)
	f.write(sentence)
	f.close()

	# Create dictionary of RNN assigned numbers to their names
	labels = {}
	f = open(labels_path, "r")
	for line in f.readlines():
		line = re.sub("\n", "", line)
		line = line.split(' ')
		name = line[0]
		key = line[1]
		labels[key] = name
	
	# Call the RNN	
	call = """java -Xms1g -Xmx1g -XX:+UseTLAB -XX:+UseConcMarkSweepGC -cp .:bin/:libs/* main.RAEBuilder \
	-DataDir data/question_type \
	-MaxIterations 20 \
	-ModelFile data/question_type/tunedTheta.rae \
	-ClassifierFile data/question_type/Softmax.clf \
	-NumCores 3 \
	-TrainModel False \
	-ProbabilitiesOutputFile """ + output_path + """\
	-TreeDumpDir data/question_type/trees"""
	os.system(call + " > output.txt 2>&1")

	# Acess the output
	f = open(output_path, "r")
	output = f.readlines()

	print "lables " + str(labels)
	print "output " + str(output)
	scores = []
	for line in output:
		sub_scores = []
		line = re.sub(", \n", '', line)
		for score_label in line.split(", "):
			score_label = score_label.split(" : ")
			key = score_label[0]
			score = score_label[1]
			sub_scores.append((key, score))
		scores.append(sub_scores)
	f.close()
	print "scores " + str(scores)

	# Sort results and match them to labels
	final = []
	for sentence in scores:
		sub = {}
		for s in sentence:
			label_key = s[0]
			score = s[1]
			label_name = labels[label_key]
			sub[label_name] = score
		sorted_scores = sorted(sub.iteritems(), key=operator.itemgetter(1))
		sorted_scores.reverse()
		final.append(sorted_scores)

	return final


s1 = "Who is Lincoln?"
s2 = "When was Lincoln born?"
s3 = "Where was Licoln born?"
s = [s1, s2, s3]

start = time.time()
x = classify(s)
print "---------------------"
print x
duration = time.time() - start
print duration
