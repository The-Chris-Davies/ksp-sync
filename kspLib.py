#header for asyncServer.py. Used to compare save files.
import StringIO
def fillTree(fileData, depth = 0):
	'''makes a tree based on the data in persistent. We use this tree to extract values.'''
	if depth == 0:
		fileData = StringIO.StringIO(fileData)
	tree = []
	for line in fileData:
		if line.strip() == '{':
			tree.append(fillTree(fileData, depth+1))
		elif line.strip() == '}':
			return tree
		else:
			tree.append(line.strip())
	return tree

def printTree(tree, depth = 0):
	'''prints the given tree, with indentation to represent depth.'''
	for node in tree:
		if type(node) == str:
			print depth*'\t' + node
		else:
			printTree(node, depth+1)

#True=Not same, False=Same
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

def remove_outer(L):
	if len(L)==1:
		return remove_outer(L[0])
	else:
		return L

def find_ind(s,L):
	#ind=-1
	#iter through list
	for i in range(len(L)):
		if getPID(s) == getPID(L[i]):
			return i
	return -1
	
def getPID(vessel):
	'''given a vessel (represented as a list), return its pid.'''
	for line in vessel:
		if line.split(' = ')[0] == 'pid':
			return line.split(' = ')[-1]
	return -1

def unTree(tree, depth = 0):
	'''Turns a tree back into a string.'''
	treeStr = ''
	for line in tree:
		if type(line) == str:
			treeStr += depth*'\t' + line + '\n'
		else:
			treeStr += depth*'\t' + '{\n' + unTree(line, depth+1) + depth*'\t' + '}\n'
	return treeStr