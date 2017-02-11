#!usr/bin/python

def fillTree(fileData, depth):
	tree = []
	for line in fileData:
		if line[depth:-1].isalpha() and line[depth:-1].isupper():
			tree.append(line[depth:-1])
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


loadData = open("persistent.sfs")
current = []	#'directory'
graph = []		#'tree'
ind = 0			#expected indentation of line
graph = fillTree(loadData, 0)
printTree(graph, 0)


loadData.close()