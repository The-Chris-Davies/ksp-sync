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

def is_new(s):
	if s in L.keys():
		if L[s][ips[client_address]]==True:
			L[s]=[False]*len(ips.keys())
			L[s][ips[client_address]]=True
			return True
		else:
			L[s][ips[client_address]]=True
			return False
	else:
		L[s]=[False]*len(ips.keys())
		L[s][ips[client_address]]=True
		return True	

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
	if len(L)>1:
		return L
	else:
		return remove_outer(L[0])

def find_ind(s,L):
	ind=-1
	
	#iter through list
	for i in range(len(L)):
		
		#If ind is VESSEL skip
		#if L[i][0].isupper():
		#	continue
		
		
		#iter through lines of VESSEL block
		for j in range(len(L[i])):
			if L[i][j].split(" - ")[0]=="pid" and L[i][j].split(" - ")[1]==s:
				return i
	
	
	

