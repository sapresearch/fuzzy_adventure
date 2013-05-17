from nose.tools import *
from fuzzy_adventure.query_decomposition.nlp_system import nlp_nlidb



"""
At the time of this writing, this example would fail with the following error
allWords, required_values, target, conditions, tables, question_type= nlp_nlidb.nlp_nlidb("What component has the maximum contribution to my backlog?")
or 
'Whos is the person you will assign most important task to?'

---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
<ipython-input-28-0b4d7cd47c03> in <module>()
----> 1 allWords, required_values, target, conditions, tables, question_type= nlp_nlidb.nlp_nlidb("What component has the maximum contribution to my backlog?")

/home/I834397/Git/fuzzy_adventure/fuzzy_adventure/query_decomposition/nlp_system/nlp_nlidb.py in nlp_nlidb(question)
     35
     36         '''Creating Links between allWords and tables' entities'''
---> 37         tables = set(semanticNet.tables(allWords))
     38         required_values = set(semanticNet.required_values(tables, allWords))
     39         # print allWords, required_values, target, conditions, tables, question_type, question

/home/I834397/Git/fuzzy_adventure/fuzzy_adventure/query_decomposition/nlp_system/semanticNet.py in tables(allWords)
     29         tables = []
     30         foundTables = set()
---> 31         singulars = [en.noun.singular(w.lower()) for w in allWords]
     32         table_names = {'component': 'components_table', 'employee':'programmers_table', 'transaction':'transactions_table'}
     33         for word,table_name in table_names.iteritems():

AttributeError: 'NoneType' object has no attribute 'lower'


The code fails in the semanticNet module. Three ways of solving this. 
- The exception is handled in semanticNet module, in which case the calling module will probably be notified that something went wrong. In which case the test will have to check this return value to make sure the intended behaviour is executed.
- Or it is decided that the calling module should handle this exception, in which case the test will have to test this handling
- Or the calling module let it go through, in which case the test has to check that an exception is raised/let through


"""