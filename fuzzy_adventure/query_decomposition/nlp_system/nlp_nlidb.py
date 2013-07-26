import re
import sys
import string
import my_parser
from answerGenerator import answerGenerator
from fuzzy_adventure.external import en
import semanticNet
import glossary
import stanford_client
import penn_treebank_node
from fuzzy_adventure.test import load_data
from fuzzy_adventure.debug import debug

def nlp_nlidb(question):

       '''STEP1: Extracting the keywords using Parser:'''
       tree = stanford_client.to_tree(question)
       top_node = penn_treebank_node.parse(tree)
       extracted_words, Proper_Nouns = my_parser.key_words(top_node, question)
       question_type = my_parser.questionType(top_node)


       '''STEP2: Replace words with glossary terms:'''
       uniqueWords = glossary.generalizedKeywords(question, extracted_words)

       # '''STEP2.2: Extracting the related keywords:'''
       uniqueWords.append(question_type)
       '''STEP3: Adding some manually defined rules'''

       allWords, conditions, target, component_value = answerGenerator(question, uniqueWords)

       # To be handled differently, this is here only so the master branch can run.
       allWords = filter(lambda x: x != None, allWords)
       allWords = allWords + list(target)
       allWords = set(allWords)

       '''Creating Links between allWords and tables' entities'''
       tables = set(semanticNet.tables(allWords))
       '''required_values is not being used in our system anymore'''
       required_values =''

       debug.debug_statement([allWords, required_values, target, conditions, tables, question_type, Proper_Nouns, component_value])

       return allWords, required_values, target, conditions, tables, question_type, Proper_Nouns, component_value


def keyWords_allQuestions(question):

       allWords, required_values, target, conditions, tables, question_type, Proper_Nouns = nlp_nlidb(question)
       return [merge(allWords, required_values, target, conditions, tables, question_type, question, Proper_Nouns)]

def merge(allWords, required_values, target, conditions, tables, question_type, question,Proper_Nouns):
       allWords = ','.join(allWords)
       required_values = ','.join(required_values)
       target = ','.join(target)
       conditions = ','.join(conditions)
       tables = ','.join(tables)
       Proper_Nouns = ','.join(Proper_Nouns)
       values = [allWords, target, conditions, question_type, Proper_Nouns]


       formatted = []
       for v in values:
              if v != None and len(v)!=0 : formatted.append(v)
       merged = ','.join(formatted)
       return merged

def rewrite():
       path = "../nlidb/template_selectors/data2.txt"
       questions, _, types = load_data.load_data(path)
       supplemented = []
       for i,q in enumerate(questions):
              t = types[i]
              #allWords, required_values, target, conditions, tables, question_type = nlp_nlidb(q)
              #allWords = ' '.join(allWords)
              #required_values = ' '.join(required_values)
              #target = ' '.join(target)
              #conditions = ' '.join(conditions)
              #tables = ' '.join(tables)
              #values = [allWords, required_values, target, conditions, tables, question_type, q]
              values = [nlp_nlidb(q) + q]
              #formatted = []
              #for v in values:
                     #if v != None: formatted.append(v)
              data = ' '.join(values)
              data = data + "\t\t" + t
              supplemented.append(data)
       supplemented = "\n".join(supplemented)
       new_file = file('more.txt', 'a')
       new_file.write(supplemented)
       new_file.close()

def reformat():
       path = "../nlidb/template_selectors/data2.txt"
       _, _, types = load_data.load_data(path)
       path = "more.txt"
       questions = file(path, 'r').readlines()
       both = []
       for i,q in enumerate(questions):
              t = types[i]
              q = re.sub("\n", '', q)
              merged = q + "\t\t" + t
              both.append(merged)
       path = 'more.txt'
       both = "\n".join(both)
       f = file('more2.txt', 'a')
       f.write(both)
       f.close()

