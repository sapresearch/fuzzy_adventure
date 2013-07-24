# <<<<<<< HEAD
""" This program returns the key words in a sentence/question and the category of the sentence. 
@ INPUT: tree (The output of penn_treebank_node) """
from fuzzy_adventure.external import en
from fuzzy_adventure.query_decomposition import wordnet_synonym
import string
import operator
from fuzzy_adventure.debug import debug
import nltk


def questionType(tree):
    has_employee = False
    np = tree.descendent(['NP'])

    if tree.word_search('employee') or tree.word_search('one'):
        has_employee = True
    # has_which_employee = tree.word_search('one')
    has_component = tree.word_search('component')
    has_transaction = tree.word_search('transaction')
    # has_which_component = tree.word_search('components')

    # if n0.node_type in ['WHADVP','WHNP'] and n1.node_type in ['S', 'SQ']:
    if tree.word_search('who'):
        return 'employee'
    elif tree.word_search('where'):
        return 'Location'
    elif tree.word_search('when'):
        return 'Time'
    elif np and (np.word_search('which') or np.word_search('what')):
        if has_employee:
            return "employee"
        elif has_component:
            return "component"
        elif has_transaction:
            return 'transaction'
        else:
            return "component"
    elif tree.word_search('name'):
        if tree.word_search('person'):
            return 'employee'
    elif tree.word_search('name'):
        if tree.word_search('component'):
            return 'component'
    elif tree.word_search('how'):
        if tree.word_search('many'):
            return 'How_quantity'
        else:
            return 'How_quality'

def proper_nouns(question):

    PPN = []
    words = nltk.word_tokenize(question)
    tags = nltk.pos_tag(words)
    for i in range(len(tags)-1):
        if tags[i][1] == 'NNP' and tags[i+1][1] == 'NNP':
            name = (str(words[i])).upper() + ' ' + (str(words[i+1])).upper() 
            PPN.append(name)
    return PPN

def key_words(top_node, question):
    verb_labels = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
    question_type = questionType(top_node)
    PPN = proper_nouns(question)

    keyWords = dict()
    NPS=[]
    JPS =[]
    has_employee = False
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
        if node.descendent('CD'):
            nouns.add(node)

    if len(nodes)>1:    
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
                    if np.descendent('NNS'):
                        nouns.add(np.descendent('NNS'))



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

        """ Custom parsing """
        more_possesive_adjective = possesive_adjectives(question)
        all_adjs = keyWords['Adjectives and Propositions'].union(more_possesive_adjective)
        keyWords['Adjectives and Propositions'] = all_adjs

    keyWords = _formatKeyWords(keyWords)
    return keyWords, PPN

def _formatKeyWords(keyWords):
    nouns = []
    verbs = []
    adjs_prpos = []
    to_remove = []
    extracted_words = []
    # PPN = []

    # Check that at least 1 keyword was found.
    all_keywords = [item for sublist in keyWords.values() for item in sublist]
    if len(all_keywords) < 1: debug.debug_statement("No keywords found!")

    else:   
        for n in keyWords['Nouns']:
            if n!= None:
                # n_lemmatized = WN_Lemmatizer().lemmatize(n.word)
                # nouns.append(str(n_lemmatized))
                nouns.append(str(n.word))
        for v in keyWords['Verbs']:

            "remove the auxiliary verb 'to be':"
            if en.verb.infinitive(v) == 'be':
                to_remove.append(v)
            if v!= None:
                # v_stemmed = PStemmer().stem(v.word)
                # verbs.append(str(v_stemmed))
                verbs.append(str(v.word))

        for adj in keyWords['Adjectives and Propositions']:
            if adj!= None:
                adjs_prpos.append(str(adj.word))

        # for pr_n in keyWords['Proper Nouns']:
        #     if pr_n != None:
        #         PPN.append(pr_n)
        
        verbs = [x for x in verbs if x not in to_remove]

        '''combine all key words extracted for each category:'''
        extracted_words = nouns + verbs + adjs_prpos
        while '' in extracted_words:
            extracted_words.remove('')

    return extracted_words

def possesive_adjectives(question):
    no_punctuation = question.translate(string.maketrans("",""), string.punctuation)
    words = no_punctuation.split()
    possesive_adjs = ['my','your','his','her','their','its','our']
    adjective_prepositions = set()
    for w in words:
        if w in possesive_adjs:
            adjective_prepositions.append(w)
	return adjective_prepositions