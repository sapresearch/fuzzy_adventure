#/usr/bin/python
import os
import sys
import MySQLdb
import time
import re

from fuzzy_adventure.test import load_data
from fuzzy_adventure.query_decomposition import bayes, word_space, nlp
from fuzzy_adventure.query_decomposition.nlidb.template_selectors import template_type
from fuzzy_adventure.query_decomposition.nlidb.term_selectors import term_selector
from fuzzy_adventure.query_decomposition.nlp_system import nlp_nlidb

project_path = os.environ['FUZZY_ADVENTURE']


""" Main executable file for the whole system.
To use it, run the FuzzyAdventure.demo() function to let the user input questions to
the command line, or the FuzzyAdventure.test() function to find the number of questions
that it correctly classifies. """


#data_file = project_path + "/query_decomposition/nlidb/template_selectors/data2.old.txt"
#data_file = project_path + "/query_decomposition/nlidb/template_selectors/more2.txt"
data_file = project_path + "/query_decomposition/nlidb/template_selectors/questions_plus.json"

# Use Bayes classifier
model = bayes.Bayes(data_file)

# Use word space classifier
#model = word_space.WordSpace(data_file) 

tc = template_type.TemplateClassifier(model)


class FuzzyAdventure():

    @classmethod
    def demo(self, verbose=False):
        while True:
            print "Ask a question:"
            query = raw_input()
    
            verbose = re.match(".*-v", query) != None
            query = re.sub("-v", '', query)
    
            start = time.time()
            answer, lat_type = self.to_sql(query)
            #sql = sql[0]
            #answer = execute(sql)
            duration = time.time() - start
    
            if verbose:
                print "Time: " + str(round(duration, 3))
                #print "SQL: " + str(sql)
                print "LAT Type: " + str(lat_type)
            print "Answer: " + str(answer) + "\n"
        return None
    
    @classmethod
    def test(self):
        text, targets = load_data.load_questions(data_file)
        text, targets = text[1::2], targets[1::2]
        correct = 0.
        for i,t in enumerate(text):
            target = targets[i]
            answer, key = self.to_sql(t)
            print "Question: ", t
            # print "Answer:", answer
            print "Predicted/target: ", key, target
            if key == target:
                correct += 1.
        print "Accuracy: " + str(correct/len(text))        
        print "Total tested: " + str(len(text))
    

    @classmethod
    def to_sql(self, nl_query):
        supplemented, _, _, _, _, _ = nlp_nlidb.nlp_nlidb(nl_query)
        # supplemented = nlp_nlidb.nlp_nlidb(nl_query)
        print supplemented 
        sql, lat_type = tc.template(supplemented)
        keywords = nlp.tokens(nl_query)
        keywords = nlp.remove_stopwords(keywords)
        answer = term_selector.TermSelector.fill_in_the_blanks(sql, keywords)
        return answer, lat_type



#q = "Who is my best employee?"
FuzzyAdventure.test()
#q = "How long does it take to close a high priority ticket?"
#FuzzyAdventure.to_sql(q)
#FuzzyAdventure.demo()