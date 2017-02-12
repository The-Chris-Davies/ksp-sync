#!usr/bin/python

import pickle
from kspLib import *

#try to load shipVers and serverGraph from file
try:
	saveData = open("serverSave.pkl")
	serverGraph, shipVers = pickle.load(saveData)
	saveData.close()
except:
	serverGraph = []
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


#this is where we send the stuff back

saveData = open("serverSave.pkl", 'w')
pickle.dump((serverGraph, shipVers), saveData)
saveData.close()

print shipVers

print getPID(clientGraphReduced[0])

#True=Not same, False=Same
print compare_tree(clientGraphReduced,serverGraph)
#print clientGraph
