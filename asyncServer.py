#!usr/bin/python

from kspLib import *
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
#printTree(testTree)
print compare_vessel(clientGraph,serverGraph)
#print clientGraph