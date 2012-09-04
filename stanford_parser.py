class StamfordNode():
    depth = 0
    siblings = []
    
    def __init__(self, type = 'ROOT', word = None, index = 1, probability = 0.0, children = [], parent = None):
        self.type = type
        self.word = word
        self.index = index
        self.probability = probability
        self.children = children
        self.parent = parent
        
    def getType(self):
        return self.type

    def getWord(self):
        return self.word

    def wordIndex():
        return self.position

    def getProbability():
        return self.probability

    def children():
        return children

    def siblings():
        return

    def depth():
        return

def parseString(tree):
    start = '('
    close = ')'
    brac = '['
    node_arr = []
    word_count = 0
    depth = 0
    #siblings

    arr = tree.split()
    stack = []
    par_node = 1
    #print curr_node
    for element in arr:
        #print curr_node
        if element[0] == start or element[0] == brac:
            stack.append(element)
            par_node = par_node + 1
        elif element[-1] == close:
            count = element.count(close)
            w = element[:-count]
            #print w
            p = ''
            t = ''
            word_count = word_count + 1
            i = word_count
            for j in range(count):
                #print "range " + str(range(count))
                #print j
                ele = stack.pop()
                print ele
                if ele[0] == brac:
                    j = j + 1
                    p = element[1:-1]
                    #print p
                elif ele[0] == start:
                    t = element[1:]
                    #print t
                    node_arr.append(StamfordNode(t, w, i, p, [], par_node))
                    #print "par "
    return node_arr