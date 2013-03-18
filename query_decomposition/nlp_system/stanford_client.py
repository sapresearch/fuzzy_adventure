import pycurl
import cStringIO
import xmlrpclib
import re

def to_tree(sentence):
	sentence = re.sub("\?", '', sentence)
	proxy = xmlrpclib.ServerProxy('http://localhost:9001')
	tree = proxy.tree(sentence)
	return tree


def tagged_labeled_yield(sentence):
    sentence = re.sub("\?", '', sentence)
    proxy = xmlrpclib.ServerProxy('http://localhost:9001')
    data = proxy.tagged(sentence)

    l = list(data)
    l.pop(0)
    l.pop()
    data = "".join(l)
    data = [x.replace("[","").replace("]","") for x in data.split(",")]

    tly = []
    for line in data:
        l = line.split(" ")
        d = {}
        for i in l:
            if i == '':
                continue
            pair = i.split('=')
            d[pair[0]] = pair[1]
        tly.append(d)

    return tly

def flatten(sentence):
    sentence = re.sub("\?", '', sentence)
    proxy = xmlrpclib.ServerProxy('http://localhost:9001')
    data = proxy.flatten(sentence)

    return data