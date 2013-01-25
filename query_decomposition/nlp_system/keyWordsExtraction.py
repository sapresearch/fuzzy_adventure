
# This program returns the key words in a sentence/question and the category of the sentence. 
#@ INPUT: tree (The output of penn_treebank_node)

def questionType(tree):

    np = tree.descendent(['NP'])
    has_which_employee = tree.word_search('employee')
    has_which_component = tree.word_search('component')or tree.word_search('components')

    if tree.word_search('who'):
        return 'Employee'
    elif tree.word_search('where'):
        return 'Location'
    elif tree.word_search('when'):
        return 'Time'
    elif np and (tree.word_search('which') or tree.word_search('what')):
        if has_which_employee:
            return "Employee"
         # or np.word_search('person') or np.word_search('member of the team') or np.word_search('team member') or np.word_search('member')
        if has_which_component:
            return "Component"
    elif tree.word_search('name'):
        if tree.word_search('person'):
            return 'Employee'
    elif tree.word_search('name'):
        if tree.word_search('component'):
            return 'component'

def keyWordsExtraction(top_node):

    question_type = questionType(top_node)
    keyWords = set()
    NPS=[]
    JPS =[]
    # query = False

    i = 0
    nodes=[]
    while top_node.node_index(i):
        nodes.append(top_node.node_index(i))
        i = i+1

    for node in nodes:
        if node.descendent ('NP'):
            NPS.append(node)
        if node.descendent('ADJP'):
            JPS.append(node)
        
    VP = node.descendent(['VP'])
    PP = node.descendent(['PP'])

    if top_node.node_type in ['SBARQ','SBAR','S']:

            if VP:
                if VP.descendent('VBZ'):
                    keyWords.add(VP.descendent('VBZ'))

            for np in NPS:
                if np.descendent('NP'):
                    keyWords.add(np.descendent('NP'))
                if np.descendent('JJS'):
                    keyWords.add(np.descendent('JJS'))
                if np.descendent('NN'):
                    keyWords.add(np.descendent('NN'))
                if np.descendent('NNS'):
                    keyWords.add(np.descendent('NNS'))
                if np.descendent('NNP'):
                    keyWords.add(np.descendent('NNP'))


            for jp in JPS:
                # adj_node = None
                if jp.descendent('RBS'):
                    keyWords.add(jp.descendent('RBS'))
                if jp.descendent('JJ'):
                    keyWords.add(jp.descendent('JJ'))
                elif jp.descendent('JJS'):
                    keyWords.add(jp.descendent('JJS'))


            if PP:
                if PP.descendent('IN'):
                    keyWords.add(PP.descendent('IN'))
                if PP.descendent('NN'):
                    keyWords.add(PP.descendent('NN'))


    return keyWords, question_type

