#!usr/bin/python

from kspLib import *
#make backup of data
#make server tree


saveData = open("persistent-NEW.sfs")
oldData = open("backup.sfs", 'w')
serverGraph = fillTree(saveData)
oldData.write(saveData.read())
saveData.close()
oldData.close()

client_address="184.68.166.106"

ips={"184.68.166.106":0,"24.87.29.11":1}
L={}




#serverData = open("persistent-NEW.sfs")
#serverGraph = fillTree(serverData)
#serverData.close()


#GET THIS FROM CLIENT PUSH
#make client tree
clientData = open("persistent.sfs")
clientGraph = fillTree(clientData)
clientData.close()

clientGraphReduced = remove_outer(getFromTree(clientGraph, ["GAME", "FLIGHTSTATE", "VESSEL"]))
serverGraphReduced = remove_outer(getFromTree(serverGraph, ["GAME", "FLIGHTSTATE", "VESSEL"]))

#print len(testTree)
#print len(testTree2)

for i in range(len(clientGraphReduced)):
	pid=getPID(clientGraphReduced[i])
	
	if (find_ind(pid,serverGraphReduced)==-1):
		#NOT IN SERVER
		pass
	
	else:
		
	
	



#printTree(testTree)

print getPID(clientGraphReduced[0])

#True=Not same, False=Same
print compare_tree(clientGraphReduced,serverGraphReduced)
#print clientGraph
