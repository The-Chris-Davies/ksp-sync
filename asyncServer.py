#!usr/bin/python

from kspLib import *
#make backup of data
saveData = open("server.sfs")
oldData = open("backup.sfs", 'w')
oldData.write(saveData.read())
saveData.close()
oldData.close()

client_address="184.68.166.106"

ips={"184.68.166.106":0,"24.87.29.11":1}
L={}



#make server tree
serverData = open("persistent-NEW.sfs")
serverGraph = fillTree(serverData)
serverData.close()

#make client tree
clientData = open("persistent.sfs")
clientGraph = fillTree(clientData)
clientData.close()

testTree = getFromTree(clientGraph, ["GAME", "FLIGHTSTATE", "VESSEL"])

#printTree(testTree)
print compare_tree(clientGraph,serverGraph)
#print clientGraph
