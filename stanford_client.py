import pycurl
import cStringIO


# The Staford Parser is run on a separate service.
# This client interfaces with it and returns the parsed sentence.
def to_tree(sentence):
	stanford_server = pycurl.Curl()

	server = "http://localhost:3000/sentence/parse/"
	sentence = sentence.replace(" ", "_")
	url = server + sentence
	stanford_server.setopt(pycurl.URL, url)

	buf = cStringIO.StringIO()
	stanford_server.setopt(stanford_server.WRITEFUNCTION, buf.write)

	stanford_server.perform()
	parsed = buf.getvalue()
	return parsed
