#!usr/bin/python

def fillTree(fileData, depth):
	tree = []
	for line in fileData:
		if line[depth:-1] == '{':
			tree.append(fillTree(fileData, depth+1))
		elif line[depth-1:-1] == '}':
			return tree
		else:
			tree.append(line[depth:-1])
	return tree
def printTree(tree, depth):
	for node in tree:
		if type(node) == str:
			print depth*'\t' + node
		else:
			printTree(node, depth+1)

#main
#make backup of data
saveData = open("server.sfs")
oldData = open("backup.sfs", 'w')
oldData.write(saveData.read())
saveData.close()
oldData.close()

#make server tree
serverData = open("server.sfs")
serverGraph = fillTree(serverData, 0)
serverData.close()

#make client tree
clientData = open("persistent.sfs")
clientGraph = fillTree(clientData, 0)
clientData.close()