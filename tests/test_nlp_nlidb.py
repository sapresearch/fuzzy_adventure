from nose.tools import *
from fuzzy_adventure.query_decomposition.nlp_system import nlp_nlidb.py


allWords, required_values, target, conditions, tables, question_type= nlp_nlidb.nlp_nlidb("What component has the maximum contribution to my backlog?")