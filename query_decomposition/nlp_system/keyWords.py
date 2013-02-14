# This program returns the key words in a sentence/question and the category of the sentence. 
#@ INPUT: tree (The output of penn_treebank_node)
import sys
sys.path.append("../")
import wordnet_synonym 
import penn_treebank_node
from stanford_client import to_tree
import penn_treebank_node
import string

def questionType(tree):
    np = tree.descendent(['NP'])

    has_employee = tree.word_search('employee')
    # has_which_employee = tree.word_search('one')
    has_component = tree.word_search('component')
    has_transaction = tree.word_search('transaction')
    # has_which_component = tree.word_search('components')

    # if n0.node_type in ['WHADVP','WHNP'] and n1.node_type in ['S', 'SQ']:
    if tree.word_search('who'):
        return 'Employee'
    elif tree.word_search('where'):
        return 'Location'
    elif tree.word_search('when'):
        return 'Time'
    elif np and (np.word_search('which') or np.word_search('what')):
        if has_employee:
            return "Employee"
        elif has_component:
            return "Component"
        elif has_transaction:
            return 'transaction'
        else:
            return "Component"
    elif tree.word_search('name'):
        if tree.word_search('person'):
            return 'Employee'
    elif tree.word_search('name'):
        if tree.word_search('component'):
            return 'Component'
    elif tree.word_search('how'):
        if tree.word_search('many'):
            return 'How_quantity'
        else:
            return 'How_quality'
    

def keyWordsExtraction(top_node):

    verb_labels = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
    question_type = questionType(top_node)
    keyWords = dict()
    NPS=[]
    JPS =[]
    # query = False
    nouns = set()
    verbs = set()
    prepositions_Adjs = set()

    i = 0
    nodes=[]
    while top_node.node_index(i):
        nodes.append(top_node.node_index(i))
        i = i+1

    for node in nodes:
        # To make sure the proper noun will be always added to the keywords.
        if wordnet_synonym.is_proper_noun(node):
            nouns.add(node)
        if node.descendent ('NP'):
            NPS.append(node)
        if node.descendent('ADJP'):
            JPS.append(node)
        
    VP = nodes[1].descendent(['VP'])
    PP = nodes[1].descendent(['PP'])



    if top_node.node_type in ['SBARQ','SBAR','S']:

            
            if VP:
                for v in verb_labels:
                    if VP.descendent(v):

                        verbs.add(VP.descendent(v))


            for np in NPS:
                if np.descendent('NP'):
                    nouns.add(np.descendent('NP'))
                if np.descendent('JJS'):
                    nouns.add(np.descendent('JJS'))
                if np.descendent('NN'):
                    nouns.add(np.descendent('NN'))
                if np.descendent('NNS'):
                    nouns.add(np.descendent('NNS'))
                if np.descendent('NNP'):
                    nouns.add(np.descendent('NNP'))


            for jp in JPS:
                # adj_node = None
                if jp.descendent('RBS'):
                    prepositions_Adjs.add(jp.descendent('RBS'))
                if jp.descendent('JJ'):
                    prepositions_Adjs.add(jp.descendent('JJ'))
                elif jp.descendent('JJS'):
                    prepositions_Adjs.add(jp.descendent('JJS'))


            if PP:
                # if PP.descendent('IN'):
                #     keyWords.add(PP.descendent('IN'))
                if PP.descendent('NN'):
                    prepositions_Adjs.add(PP.descendent('NN'))

    keyWords = {'Nouns':nouns, 'Verbs':verbs, 'Adjectives and Propositions':prepositions_Adjs} 
    return keyWords, question_type


def formatKeyWords(question):
    buf=[]
    nouns = []
    verbs = []
    adjs_prpos = []
    tree = to_tree(question)
    keyWords_allNull = 0
    print tree
    root = penn_treebank_node.parse(tree)
    keyWords, question_type = keyWordsExtraction(root)
    # print question_type
    possesive_adjs = ['my','your','his','her','their','its','our']
    # check for all three keys of the dictionary if they are empty:
    if ([a for a in keyWords.values() if a == []]):
        keyWords_allNull = keyWords_allNull  + 1
    if keyWords_allNull==3:
        print("No keywords found! \r\n")
    else:
            # temp = []
        for n in keyWords['Nouns']:
            if n!= None:
                # n_lemmatized = WN_Lemmatizer().lemmatize(n.word)
                # nouns.append(str(n_lemmatized))
                nouns.append(str(n.word))
        for v in keyWords['Verbs']:
            if v!= None:
                # v_stemmed = PStemmer().stem(v.word)
                # verbs.append(str(v_stemmed))
                verbs.append(str(v.word))

        for adj in keyWords['Adjectives and Propositions']:
            if adj!= None:
                adjs_prpos.append(str(adj.word))

        # print temp
        q_noPunc = question.translate(string.maketrans("",""), string.punctuation)
        words = q_noPunc.split()
        for w in words:
            if w in possesive_adjs:
                adjs_prpos.append(w)

    return nouns,verbs, adjs_prpos, question_type
