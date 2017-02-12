#!usr/bin/python

import cPickle as pickle
from kspLib import *
import socket
import sys


#try to load shipVers and serverGraph from file
try:
	saveData = open("serverSave.pkl")
	serverGraph, shipVers = pickle.load(saveData)
	saveData.close()
except:
	serverGraph = []
	shipVers = {}


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((socket.gethostname(), 8988))
serversocket.listen(5)

#client_address="184.68.166.106"



while True:
	#accept connections from outside
	connection, client_address = serversocket.accept()
	
	print 'connection from',client_address
	
	totaldata=""
	
	# Receive the data in small chunks and retransmit it
	while True:
		data = connection.recv(2048)
		if data:
			totaldata+=data
		else:
			break
	
	clientGraph = fillTree(totaldata)
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
	
	returndata=pickle.dumps(serverGraph)
	connection.sendall(returndata)
	
	
	

saveData = open("serverSave.pkl", 'w')
pickle.dump((serverGraph, shipVers), saveData)
saveData.close()

