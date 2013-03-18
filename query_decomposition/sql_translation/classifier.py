import os
project_path = os.environ['FUZZY_ADVENTURE']
import sys
sys.path.append(project_path + '/query_decomposition/nlp_system')
import preprocessing as pp
from preprocessing import Preprocessing
import penn_treebank_node as ptn
from queue import Queue
from collections import Counter
import pandas as pd
from pandas import DataFrame, Series
import numpy as np
import stanford_client as sc

"""
This file is meant to replace query_classifier in the short term or at the very least supplement it. 'query_classifier' has shown some limitations in term of flattening the parsed tree and losing the structure.
First draft of this will be crude, using a simple product rule of probabilities
p(y|x) = p(x|y)p(y) / p(x)
'y' represents an sql skeleton
'x' represents a list of rules in Context Free Grammar (e.g. NP -> DT NN)
The goal is to predict which skeleton it belongs too based on the parsed tree from the question (parsed as PennTree by the stanford parser)

argmax p(y|x) = argmax p(x|y)p(y), we can drop p(x) since it's a constant and doesn't change argmax
So we're choosing the skeleton that will yield the highest probability. In doing so, we can order the seletons, pick the top three, normalize the probabilities and have a confidence estimator.
"""

class TreeClassifier(object):

    def __init__(self, laplace = 0):
        self.laplace = laplace


    def fit(self, trees, labels):
        self.apriori = self.a_priori(labels)
        self.posteriori = self.a_posteriori(trees, labels)


    def predict(self, tree):
        tree_rules = self.extract_rules(sc.to_tree(tree))

        df = DataFrame(columns=['label', 'prob'])
        gb = self.posteriori.groupby('label')


        for key, indexes in gb.groups.items():
            group_df, missing_prob = self.apply_smoothing(self.posteriori.ix[indexes], tree_rules)

            apriori_prob = self.apriori[self.apriori.label == key]['freq'].values[0]
            prob = apriori_prob

            for rule in tree_rules:
                prob_evidence = group_df[group_df.rule == rule]['freq']
                if len(prob_evidence) == 0:
                    prob_evidence = missing_prob
                else:
                    prob_evidence = prob_evidence.values[0]
                prob *= prob_evidence

            post = DataFrame({'label':[key], 'prob':[prob]})
            df = df.append(post)

        df.index = np.arange(df.index.size)
        df = df.sort(columns='prob', ascending=False)
        return df.ix[df['prob'].idxmax()]


    def a_priori(self, labels):
        counted_labels = Counter(labels)
        apriori = DataFrame(counted_labels.most_common())
        apriori['freq'] = apriori[1] / float(apriori[1].sum())
        apriori.columns = ['label','count','freq']
        return apriori


    def a_posteriori(self, trees, labels):
        rules = self.count_rules(trees, labels)
        index1 = []
        index2 = []
        count = []
        for rule in rules:
            for key, value in rule.values()[0].items():
                index1.append(rule.keys()[0])
                index2.append(key)
                count.append(value)

        e_df = DataFrame({'label':index1, 'rule':index2, 'count':count})

        return e_df



    def apply_smoothing(self, group_df, tree_rules):
        t = RuleCounter(tree_rules)
        tree_rules = t.counter.keys()
        filtered = group_df.ix[tree_rules]
        absent = filtered[filtered['count'].isnull()]

        num_missing = absent.index.size

        group_df['count'] = group_df['count'] + 1
        group_size = group_df['count'].sum()

        group_df['freq'] = group_df['count'] / float(num_missing + group_size)

        if num_missing == 0:
            return group_df, None
        else:
            missing_prob = (1 - group_df.freq.sum()) / num_missing
            return group_df, missing_prob



    def count_rules(self, trees, labels):
        df = DataFrame(zip(trees, labels), columns=['tree', 'label'])
        gb = df.groupby('label')

        rules_df = []
        for group, indexes in gb.groups.items():
            rules = []
            for index in indexes:
                tree = df.ix[index]['tree']
                rules += [rule for rule in self.extract_rules(tree)]
            rules_count = RuleCounter(rules)
            rules_df.append({group: rules_count.counter})

        return rules_df


    def extract_rules(self, tree):
        tree_rules = []
        tree = ptn.parse(tree)
        queue = Queue()
        queue.push(tree)

        while not queue.empty():
            t = queue.pop()
            rule = Rule(t.node_type, [])

            for child in t.children:
                queue.push(child)
                rule.add_child(child.node_type)

            tree_rules.append(rule)

        return np.array(tree_rules)




class Rule(object):
    """
    A rule is a relation between a node and its children in a parsed tree. 
    A node will have 1 or more children (e.g. NP -> DT NN)
    No restriction is imposed on rules such as beeing terminal or not.
    A terminal rule is a tag that leads to a word (e.g. DT -> The)
    A parent without child will be a terminal rule.
    """

    def __init__(self, parent, children):
        """        
        Param
            parent: The parent of the children
            children: List of children. Can be of any length
        """
        if parent is None:
            raise RuntimeError("'parent' cannot be None") 
        if children is None:
            raise RuntimeError("'children' cannot be None. Can be an empty list.") 
        if type(children) is not type([]):
            raise RuntimeError("'children' must be of type list.") 

        self.parent = str(parent)
        self.children = children


    def add_child(self, child):
        """
        Simple method to add a child.
        Param
            child: Child to add to the list
        Return 
            True if adding was successful, False otherwise
        """
        if child is not None:
            self.children.append(child)
        return child in self.children


    def __eq__(self, rule):
        """
        Check to see if another is equals
        Param
            rule: The rule we want to test against
        Return
            True if parents and children are equals. False otherwise.
        """
        if type(rule) is type(self):
            return self.__dict__ == rule.__dict__
        return False


    def as_tuple(self):
        return (self.parent,) + tuple(self.children)



    def __repr__(self):
        string = str(self.parent)
        if len(self.children) > 0:
            string += "->"
        for child in self.children:
            string += child + " "

        return string



class RuleCounter(object):
    """
    Simulate behaviour of Counter class. Had to implement this because
    even though rules are not the same in memory, it doesn't matter for our
    needs. 
    This class will take a set of objects and count based on the content.
    The object is compared with the '==' operator, thus it should
    overwrite the __eq__ method for desired equality.
    """

    def __init__(self, rules):
        """
        Param
            rules: A list of Rule object
        """
        self.counter = {}
        for rule in rules:
            self.add_rule(rule)


    def add_rule(self, rule):
        """
        Add or increment the count of the specified object.
        Param
            rule: The rule to add or increment.
        """
        for key in self.counter.keys():
            if rule == key:
                self.counter[key] += 1
                return
        self.counter[rule] = 1





originals, skeletons, trees = Preprocessing.generalize_sql()
tc = TreeClassifier()
tc.fit(trees, skeletons)
tc.predict('Who is the most productive person on my team?')



