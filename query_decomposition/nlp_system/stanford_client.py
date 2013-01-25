import pycurl
import cStringIO
import xmlrpclib
import re

def to_tree(sentence):
	sentence = re.sub("\?", '', sentence)
	proxy = xmlrpclib.ServerProxy('http://localhost:9001')
	tree = proxy.tree(sentence)
	return tree
