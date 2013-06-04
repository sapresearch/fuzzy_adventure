#/usr/bin/python
import os
import sys
#import MySQLdb
import time
import re

from optparse import OptionParser, OptionGroup
from fuzzy_adventure.test import load_data
from fuzzy_adventure.query_decomposition import bayes, word_space, nlp
from fuzzy_adventure.query_decomposition.nlidb.template_selectors import template_type
from fuzzy_adventure.query_decomposition.nlidb.term_selectors import term_selector
from fuzzy_adventure.query_decomposition.nlp_system import nlp_nlidb
from fuzzy_adventure.query_decomposition.classifier import TemplateClassifier
from sklearn import svm
from sklearn import linear_model
from debug import debug

""" Main executable file for the whole system. """

class FuzzyAdventure():

    @classmethod
    def demo(self, verbose=False):
        print "Ask a question or type exit() to exit:"
        query = raw_input()
        while not re.match("exit()", query): 

            start = time.time()
            answer, category = self.to_sql(query)
            duration = time.time() - start

            if verbose:
                print "Time: " + str(round(duration, 3))
                print "LAT Type: " + str(category)
            print "Answer: " + str(answer) + "\n"
            print "------------------------------"
            print "Ask a question or type exit() to exit:"
            query = raw_input()


    @classmethod
    def to_sql(self, nl_query):
        sql, category = FuzzyAdventure.tc.template(nl_query)
        keywords = nlp.tokens(nl_query)
        keywords = nlp.remove_stopwords(keywords)
        answer = term_selector.TermSelector.fill_in_the_blanks(sql, keywords)

        return answer

    @classmethod
    def web_demo(self, nl_query, data_file="questions_plus.json"):
        project_path = os.environ['FUZZY_ADVENTURE']
        data_directory = project_path + "/query_decomposition/nlidb/template_selectors/"
        FuzzyAdventure.data_file = data_directory + data_file

        model = linear_model.LogisticRegression()
        FuzzyAdventure.set_classifier(model, FuzzyAdventure.data_file)

        answer = self.to_sql(nl_query)

        return answer

    @classmethod
    def set_classifier(self, model, data_file):

        # If the data file is different than before, delete the classifier to recreate it
        if hasattr(FuzzyAdventure, "data_file"):
            if FuzzyAdventure.data_file != data_file:
                delattr(FuzzyAdventure, "model")
        else:
            FuzzyAdventure.data_file = data_file

        # Only create a classifier if none were existant or if a new model is passed
        if not hasattr(FuzzyAdventure, "model") or not isinstance(FuzzyAdventure.model.model, model.__class__):
            debug.debug_statement('New classifier created with model %s' % model.__class__.__name__)
            FuzzyAdventure.model = TemplateClassifier(data_file, model, test_size=0.2)
            FuzzyAdventure.model.fit()
            FuzzyAdventure.tc = template_type.TemplateClassifier(FuzzyAdventure.model)
        else:
            debug.debug_statement('No new classifier created')

def main():

    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)

    usage_group = OptionGroup(parser, "Behaviour Options - Use only one")
    usage_group.add_option("-t", "--test", action="store_true", dest="test", default=False, help="Run a test on the program")
    usage_group.add_option("-d", "--demo", action="store_true", dest="demo", default=False, help="Demo the program")
    usage_group.add_option("-q", "--question", dest="question", metavar="QUESTION", help="specify a question to convert to SQL. Example: -q=\"How long does it take to close a high priority ticket?\"")
    parser.add_option_group(usage_group)

    debug_group = OptionGroup(parser, "Debug Options")
    debug_group.add_option("--debug", action="store_true", dest="debug", default=False, help="Debug switch to print debug statements")
    parser.add_option_group(debug_group)

    parser.add_option("-f", "--file", dest="file", default="questions_plus.json", metavar="DATAFILE", help="specify a file (located in the data directory query_decomposition/nlidb/template_selectors/) that you would like to use as input to the program. Default is 'questions_plus.json'")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False)


    (option, args) = parser.parse_args()

    if option.debug:
        debug.debug_on()

    project_path = os.environ['FUZZY_ADVENTURE']
    data_directory = project_path + "/query_decomposition/nlidb/template_selectors/"
    FuzzyAdventure.data_file = data_directory + option.file

    model = linear_model.LogisticRegression()
    FuzzyAdventure.set_classifier(model, FuzzyAdventure.data_file)


    if option.test:
        print 'Score:', FuzzyAdventure.model.score()
    if option.question:
        print FuzzyAdventure.model.predict(option.question)
    if option.demo:
        FuzzyAdventure.demo(option.verbose)

    if not (option.question or option.demo or option.test):
        print "You must enter a Behaviour Option for the program to perform. For more details run 'python executable.py --help'"

    if option.debug:
        debug.debug_off()

if __name__=="__main__":
    main()

