#!usr/bin/python

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

def check(t,s):
	for i in t:
		if i[:len(s)]==s:
			return i[len(s):]
	return false

def compare_vessel(old,new):
	#update=False
	for i in range(len(old)):
		if (old[i].isupper()):
			if (compare_vesel(old[i+1],new[new.index(old[i+1])])):
				return True
			
		else:
			for j in range(len(old[i])):
				if (old[i][j]=="="):
					if (check(new,old[i][:j])==False):
						#Doesn't exist
					else if (old[i][j+1:]==check(new,old[i][:j]):
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
			print parents[0]
			newTree.append(getFromTree(tree[i+1], parents[1:]))
	return newTree




#main
#make backup of data
saveData = open("server.sfs")
oldData = open("backup.sfs", 'w')
oldData.write(saveData.read())
saveData.close()
oldData.close()

#make server tree
serverData = open("server.sfs")
serverGraph = fillTree(serverData)
serverData.close()

#make client tree
clientData = open("persistent.sfs")
clientGraph = fillTree(clientData)
clientData.close()

testTree = getFromTree(clientGraph, ["GAME", "FLIGHTSTATE", "VESSEL"])
printTree(testTree)
