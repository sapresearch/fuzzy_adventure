#/usr/bin/python
import os
import sys
#import MySQLdb
import time
import re

from optparse import OptionParser
from fuzzy_adventure.test import load_data
from fuzzy_adventure.query_decomposition import bayes, word_space, nlp
from fuzzy_adventure.query_decomposition.nlidb.template_selectors import template_type
from fuzzy_adventure.query_decomposition.nlidb.term_selectors import term_selector
from fuzzy_adventure.query_decomposition.nlp_system import nlp_nlidb

""" Main executable file for the whole system. """

class FuzzyAdventure():

    @classmethod
    def demo(self, verbose=False):
        print "Ask a question or type exit() to exit:"
        query = raw_input()
        while not re.match("exit()", query): 

            start = time.time()
            answer, lat_type = self.to_sql(query)
            duration = time.time() - start

            if verbose:
                print "Time: " + str(round(duration, 3))
                print "LAT Type: " + str(lat_type)
            print "Answer: " + str(answer) + "\n"
            print "------------------------------"
            print "Ask a question or type exit() to exit:"
            query = raw_input()

    @classmethod
    def test(self, verbose=False):
        text, targets = load_data.load_questions(self.data_file)
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
        allWords, _, _, _, _, _, _ = nlp_nlidb.nlp_nlidb(nl_query)
        supplemented = ' '.join(allWords)
        # supplemented = nlp_nlidb.nlp_nlidb(nl_query)
        print supplemented 
        sql, lat_type = FuzzyAdventure.tc.template(supplemented)
        keywords = nlp.tokens(nl_query)
        keywords = nlp.remove_stopwords(keywords)
        answer = term_selector.TermSelector.fill_in_the_blanks(sql, keywords)
        return answer, lat_type

def main():

    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-t", "--test", action="store_true", dest="test", default=False, help="Run a test on the program")
    parser.add_option("-d", "--demo", action="store_true", dest="demo", default="False", help="Demo the program")
    parser.add_option("-q", "--question", dest="question", metavar="QUESTION", help="specify a question to convert to SQL. Example: -q=\"How long does it take to close a high priority ticket?\"")
    parser.add_option("-f", "--file", dest="file", default="questions_plus.json", metavar="DATAFILE", help="specify a file (located in the data directory query_decomposition/nlidb/template_selectors/) that you would like to use as input to the program. Default is 'questions_plus.json'")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False)
    parser.add_option("--wordspace", action="store_true", dest="wordspace", default=False, help="Use the wordspace classifier instead of the Bayes classifier. Default=False")

    (option, args) = parser.parse_args()


    project_path = os.environ['FUZZY_ADVENTURE']
    data_directory = project_path + "/query_decomposition/nlidb/template_selectors/"
    FuzzyAdventure.data_file = data_directory + option.file

    if option.wordspace:
        # Use word space classifier
        FuzzyAdventure.model = word_space.WordSpace(FuzzyAdventure.data_file)
    else:
        # Use Bayes classifier
        FuzzyAdventure.model = bayes.Bayes(FuzzyAdventure.data_file)

    FuzzyAdventure.tc = template_type.TemplateClassifier(FuzzyAdventure.model)

    if option.test:
        FuzzyAdventure.test(option.verbose)
    if option.question:
        FuzzyAdventure.to_sql(option.question)
    if option.demo:
        FuzzyAdventure.demo(option.verbose)

    if not (option.question or option.demo or option.test):
        print "You must enter an option for the program to perform. For more details run 'python executable.py --help'"

if __name__=="__main__":
    main()

