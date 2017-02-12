#!usr/bin/python

from kspLib import *
#make backup of data
saveData = open("server.sfs")
oldData = open("backup.sfs", 'w')
serverData=saveData.read()
oldData.write(saveData.read())
saveData.close()
oldData.close()

client_address="184.68.166.106"

ips={"184.68.166.106":0,"24.87.29.11":1}
L={}



#make server tree
#serverData = open("persistent-NEW.sfs")
serverGraph = fillTree(serverData)
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
	



#printTree(testTree)

#True=Not same, False=Same
print compare_tree(testTree,testTree2)
#print clientGraph
