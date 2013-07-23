import random

# TODO Keep the roots created and make sure that every new family has a new one.
def generate_software_family(root_id):
	family = generate_random_tree(root_id, 0)
	familyList = []
	for member in flatten(family):
		familyList.append(Software(member))
	return familyList
	
	
def generate_random_tree(node_id, generation):
	if generation <= 3:
		nb_children = random.randint(0,5)
	else:
		nb_children = 0
	children = []
	for child in range(nb_children):
		children.append(generate_random_tree(child, generation + 1))
	node = (str(node_id) + str(generation), children)
	return node
	
def flatten(root):
	pathList = []
	pathList.append(root[0])
	
	for child in root[1]:
		childrenList = flatten(child)
		for i in range(len(childrenList)):
			#print 'childrenList', childrenList[i]
			childrenList[i] = root[0] + '-' + childrenList[i]
		
		pathList += (childrenList)
	#if (root[1] == []):
	#	pathList.append(str(root[0]))
		#print pathList
	return pathList
				

class Software(object):
	
	def __init__(self, id):
		self.id = id
