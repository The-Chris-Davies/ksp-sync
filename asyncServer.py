#!usr/bin/python
loadData = open("persistent.sfs")
current = []	#'directory'
graph = []		#'tree'
ind = 0		#expected indentation of line
for line in loadData:
	if line[ind:-1].isalpha() and line[ind:-1].isupper():
		current.append(line[ind:-1])
		ind += 1

		print " ".join(current)

	elif line[ind-1:-1] == '}':
		current.pop()
		ind -= 1

loadData.close()