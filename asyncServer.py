#!usr/bin/python
try:
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

	while True:
		
		print "waiting for connection"
		
		#accept connections from outside
		connection, client_address = serversocket.accept()
		
		print 'connection from',client_address
		
		totalData=""
		
		# Receive the data in small chunks and retransmit it
		totalData=""
		while True:
			data = connection.recv(2048)
			#print data,"\n\n\n\n\n"
			#if data[-7:]!="abcdefg":
			totalData+=data
			if totalData[-7:]=="abcdefg":
				break
		totalData=totalData[:-7]
		#print totalData
		
		#totalData = connection.recv(81920)
		#print totalData
		

		print "data recieved"
		
		clientGraph = fillTree(totalData)
		clientGraphReduced = getFromTree(clientGraph, ["GAME", "FLIGHTSTATE", "VESSEL"])
		#clientGraphKerbal = getFromTree(clientGraph, ["GAME", "ROSTER", "KERBAL"])
		clientGraphKerbal=[]
		
		print "Data graphed"
		
		#print clientGraphReduced
		#print clientGraphReduced
		#break
		
		
		#FLIGHTSTATE
		for i in range(len(clientGraphReduced)):
			#print i
			#print clientGraphReduced[i]
			pid=getPID(clientGraphReduced[i])
			#print pid
			serverInd = find_ind(pid,serverGraph)
			if (serverInd==-1):
				#print "hi"
				#not in server
				serverGraph.append(clientGraphReduced[i])
				shipVers[pid] = [client_address[0]]
			else:
				#if client is up to date:
				if client_address[0] in shipVers[pid]:
					#check if they are the same
					if compare_tree(clientGraphReduced[i], serverGraph[serverInd]):
						#print "yo"
						serverGraph[serverInd] = clientGraphReduced[i]
						shipVers[pid] = [client_address[0]]
				else:
					#because we're updating the client
					shipVers[pid].append(client_address[0])
		#remove ships if client was up to date
		for x in serverGraph:
			if x not in clientGraphReduced and client_address[0] in shipVers[getPID(x)]:
				serverGraph.remove(x)



		
		print "Flightstate handled"
		
		#ROSTER
		for i in range(len(clientGraphKerbal)):
			name=get_name(clientGraphKerbal[i])
			serverInd = find_k_ind(name,serverGraph)
			if (serverInd==-1):
				#print "hi1"
				#not in server
				serverGraph.append(clientGraphKerbal[i])
				shipVers[name] = [client_address[0]]
			else:
				#if client is up to date:
				if client_address[0] in shipVers[name]:
					#check if they are the same
					if compare_tree(clientGraphKerbal[i], serverGraph[serverInd]):
						#print "yo1"
						serverGraph[serverInd] = clientGraphKerbal[i]
						shipVers[name] = [client_address[0]]
				else:
					#because we're updating the client
					shipVers[name].append(client_address[0])
		
		print "Roster handled"
		
		#print serverGraph
		
		#this is where we send the stuff back
		print "sending data"
		returndata=pickle.dumps(serverGraph)
		#print returndata
		connection.sendall(returndata)
		connection.sendall('abcdefg')
		print "data sent"

		saveData = open("serverSave.pkl", 'w')
		pickle.dump((serverGraph, shipVers), saveData)
		saveData.close()
	serversocket.close()
		
except Exception as exc:
	print type(exc), exc
	#connection.close()
	serversocket.close()