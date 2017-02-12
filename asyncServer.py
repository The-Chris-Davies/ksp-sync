#!usr/bin/python

import pickle
from kspLib import *

#try to load server graph from file
try:
	saveData = open("serverSave.pkl")
	serverGraph = pickle.load(saveData)
except:
	serverGraph = []

#try to load shipVers from file
try:
	shipVerData = open("IPData.pkl")
	shipVers = pickle.load(shipVerData) #whether or not the ships are updated, according to clients. True means ship is updated.
except:
	shipVers = {}

client_address="184.68.166.106"

#GET THIS FROM CLIENT PUSH
#make client tree
clientData = open("persistent.sfs")
clientGraph = fillTree(clientData)
clientData.close()

clientGraphReduced = remove_outer(getFromTree(clientGraph, ["GAME", "FLIGHTSTATE", "VESSEL"]))

for i in range(len(clientGraphReduced)):
	pid=getPID(clientGraphReduced[i])
	serverInd = find_ind(pid,serverGraph)
	if (serverInd==-1):
		#not in server
		serverGraph.append(clientGraphReduced[i])
		shipVers[pid] = [client_address]
	else:
		#if client is up to date:
		if client_address in shipVers[pid]:
			#check if they are the same
			if compare_tree(clientGraphReduced[i], serverGraph[serverInd]):
				serverGraph[serverInd] = clientGraphReduced[i]
				shipVers[pid] = [client_address]
		else:
			#because we're updating the client
			shipVers[pid].append(client_address)

print shipVers


print getPID(clientGraphReduced[0])

#True=Not same, False=Same
print compare_tree(clientGraphReduced,serverGraph)
#print clientGraph
