import pandas as pd
from pandas import DataFrame, Series
import numpy as np
import os
project_path = os.environ['FUZZY_ADVENTURE']
import sys
sys.path.append(project_path + '/query_decomposition/nlp_system')
import stanford_client
import json


def main():
    questions_filename = raw_input('>>> File name containing the questions: ')
    queries_filename = raw_input('>>> File name containing the queries: ')
    queries = json.load(open(queries_filename, 'r'))
    questions = open(questions_filename, 'r').readlines()

    q = []
    t = []
    for question in questions:
        temp = question.split('\t\t')
        q.append(temp[0])
        t.append(temp[1].strip())

    questions = []
    for (i, question) in enumerate(q):
        temp = {}
        temp['query'] = queries[t[i]]
        temp['question'] = question
        temp['tree'] = stanford_client.to_tree(question)
        questions.append(temp)

    f = open('IMS_questions.txt','w')
    f.write(json.dumps(questions, sort_keys=True,indent=4, separators=(',', ': ')))


if __name__ == '__main__':
    main()