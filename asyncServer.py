#!usr/bin/python

import cPickle as pickle
#import pickle
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
	
	print "waiting for connection"
	
	#accept connections from outside
	connection, client_address = serversocket.accept()
	
	print 'connection from',client_address
	
	totaldata=""
	
	# Receive the data in small chunks and retransmit it
	while True:
		data = connection.recv(2048)
		totaldata+=data
		if totaldata[-5:]=="abcde":
			totaldata=totaldata[:-5]
			break
	
	
	#totaldata = connection.recv(81920)
	#print totaldata
	
	print "data recieved"
	
	clientGraph = fillTree(totaldata)
	clientGraphReduced = remove_outer(getFromTree(clientGraph, ["GAME", "FLIGHTSTATE", "VESSEL"]))
	clientGraphKerbal = remove_outer(getFromTree(clientGraph, ["GAME", "ROSTER", "KERBAL"]))
	
	print "Data graphed"
	
	#print clientGraphReduced
	
	#FLIGHTSTATE
	for i in range(len(clientGraphReduced)):
		pid=getPID(clientGraphReduced[i])
		serverInd = find_ind(pid,serverGraph)
		if (serverInd==-1):
			#print "hi"
			#not in server
			serverGraph.append(clientGraphReduced[i])
			shipVers[pid] = [client_address]
		else:
			#if client is up to date:
			if client_address in shipVers[pid]:
				#check if they are the same
				if compare_tree(clientGraphReduced[i], serverGraph[serverInd]):
					#print "yo"
					serverGraph[serverInd] = clientGraphReduced[i]
					shipVers[pid] = [client_address]
			else:
				#because we're updating the client
				shipVers[pid].append(client_address)
	
	print "Flightstate handled"
	
	#ROSTER
	for i in range(len(clientGraphKerbal)):
		name=get_name(clientGraphKerbal[i])
		serverInd = find_k_ind(name,serverGraph)
		if (serverInd==-1):
			#print "hi1"
			#not in server
			serverGraph.append(clientGraphKerbal[i])
			shipVers[name] = [client_address]
		else:
			#if client is up to date:
			if client_address in shipVers[name]:
				#check if they are the same
				if compare_tree(clientGraphKerbal[i], serverGraph[serverInd]):
					#print "yo1"
					serverGraph[serverInd] = clientGraphKerbal[i]
					shipVers[name] = [client_address]
			else:
				#because we're updating the client
				shipVers[name].append(client_address)
	
	print "Roster handled"
	
	print serverGraph
	
	#this is where we send the stuff back
	print "sending data"
	returndata=pickle.dumps(serverGraph)
	print returndata
	connection.sendall(returndata)
	print "data sent"
	

	saveData = open("serverSave.pkl", 'w')
	pickle.dump((serverGraph, shipVers), saveData)
	saveData.close()
	
