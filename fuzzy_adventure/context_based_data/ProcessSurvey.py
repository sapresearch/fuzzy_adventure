
import stanford_client
import penn_treebank_node
import file

survey = open('/home/I837185/Puntis_Practices/survey.txt', 'r')
surveyAndPOS = open('/home/I837185/Puntis_Practices/surveyAndPOS.txt', 'w')

line = survey.readline()
# print line
# for line in survey,
	

# tree = stanford_client.to_tree(question)
# print tree
# top_node = penn_treebank_node.parse(tree)