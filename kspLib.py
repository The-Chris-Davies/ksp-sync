#header for asyncServer.py. Used to compare save files.
def fillTree(fileData, depth = 0):
	'''makes a tree based on the data in persistent. We use this tree to extract values.'''
	tree = []
	for line in fileData:
		if line[depth:-1] == '{':
			tree.append(fillTree(fileData, depth+1))
		elif line[depth-1:-1] == '}':
			return tree
		else:
			tree.append(line[depth:-1])
	return tree

def printTree(tree, depth = 0):
	'''prints the given tree, with indentation to represent depth.'''
	for node in tree:
		if type(node) == str:
			print depth*'\t' + node
		else:
			printTree(node, depth+1)



def compare_tree(old,new):
	#update=False
	skip=False
	for i in range(len(old)):
		if (skip==True):
			skip=False
			continue
		
		
		if (i+1==len(old)):						#SAME AS ELSE STATEMENT
			if ("=" in old[i]):
				if (old[i]!=new[i]):
					return True

		elif (type(old[i+1]))==type([]):
			skip=True
			#print old[i]
			#print new.index(old[i+1])
			if (compare_tree(old[i+1],	new[i+1]	)):
				return True
			
		else:
			if ("=" in old[i]):
				if (old[i]!=new[i]):
					return True
			
			
			
	return False
	#return update

def getFromTree(tree, parents):
	newTree = []
	'''gets the subtree from a tree. parents is a list of 'headers' that the tree is under.'''
	if parents == []:
			return tree
	for i in range(len(tree)):
		if tree[i] == parents[0]:
			newTree.append(getFromTree(tree[i+1], parents[1:]))
	return newTree
