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

shipVers={}	#whether or not the ships are updated, according to clients. True means ship is updated.


#GET THIS FROM CLIENT PUSH
#make client tree
clientData = open("persistent.sfs")
clientGraph = fillTree(clientData)
clientData.close()

clientGraphReduced = remove_outer(getFromTree(clientGraph, ["GAME", "FLIGHTSTATE", "VESSEL"]))
serverGraphReduced = remove_outer(getFromTree(serverGraph, ["GAME", "FLIGHTSTATE", "VESSEL"]))

for i in range(len(clientGraphReduced)):
	pid=getPID(clientGraphReduced[i])
	serverInd = find_ind(pid,serverGraphReduced)
	if (serverInd==-1):
		#not in server
		serverGraphReduced.append(clientGraphReduced[i])
		shipVers[pid] = [client_address]
	else:
		#if client is up to date:
		if client_address in shipVers[pid]:
			#check if they are the same
			if compare_tree(clientGraphReduced[i], serverGraphReduced[serverInd]):
				serverGraphReduced[serverInd] = clientGraphReduced[i]
				shipVers[pid] = [client_address]
		else:
			#because we're updating the client
			shipVers[pid].append(client_address)

print shipVers


print getPID(clientGraphReduced[0])

#True=Not same, False=Same
print compare_tree(clientGraphReduced,serverGraphReduced)
#print clientGraph
