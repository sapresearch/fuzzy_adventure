import sys
sys.path.append("../../")
from word_space import WordSpace

ws = WordSpace("data.txt")
q = 'What component'
print ws.classify(q)
