import stanford_parser as sp

#def extract_subject():




def extract_





str = '(ROOT (SBARQ [82.494] (WHNP [3.854] (WP [2.692] What)) (SQ [76.704] (VP [76.641] (ADVP [16.203] (RB [15.877] salesperson)) (VBD [4.662] made) (NP [48.802] (NP [13.505] (DT [0.650] the) (JJS [1.444] most) (NNS [4.188] sales)) (PP [34.891] (IN [1.850] in) (NP [32.639] (DT [0.650] the) (NNP [6.213] United) (NNP [9.167] States) (JJ [3.925] last) (NN [5.153] quarter)))))) (. [0.004] ?)))'
root = sp.parse(str)
#print root