#!usr/bin/python
import cPickle as pickle
#import pickle
from kspLib import *
import socket
import sys



try:
	serverSetttings = open("serverSettings.txt")
	port = int(serverSettings.readline()[:-1])
	print "using port", port, "found from serverSettings.txt"
except:
	print "serverSettings.txt not found! Using default port 8988"
	port = 8988


#try to load shipVers and serverGraph from file
try:
	saveData = open("serverSave.pkl")
	serverGraph, kerbalGraph, destructGraph, deletedShips, shipVers = pickle.load(saveData)
	saveData.close()
except:
	serverGraph = []
	kerbalGraph = []
	destructGraph = []
	deletedShips = []
	shipVers = {}

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((socket.gethostname(), port))
serversocket.listen(5)



while True:
	
	delete=True
	downloadOnly=False
	
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
	mode=totalData[0]
	totalData=totalData[1:]
	#print totalData
	

	print "data recieved"
	
	
	if mode=="1" or mode=="3":
		downloadOnly=True
	if mode =="2" or mode=="3":
		delete=False	
	
	if downloadOnly==False:
	
		clientGraph = fillTree(totalData)
		clientGraphVessel = getFromTree(clientGraph, ["GAME", "FLIGHTSTATE", "VESSEL"])
		clientGraphKerbal = getFromTree(clientGraph, ["GAME", "ROSTER", "KERBAL"])
		clientGraphDestructables = getFromTree(clientGraph, ["GAME", "SCENARIO"])
		clientGraphDestructablesReduced=[]
	
		for destruct in clientGraphDestructables:
			if get_name(destruct)=="ScenarioDestructibles":
				clientGraphDestructablesReduced=destruct[2:]
			
	
		#clientGraphKerbal=[]
	
		print "Data graphed"
		#print "\n",clientGraphDestructablesReduced,"\n";
		#print clientGraphVessel
		#print clientGraphVessel
		#break
	
	
		#FLIGHTSTATE
		for i in range(len(clientGraphVessel)):
			#print i
			#print clientGraphVessel[i]
			pid=getPID(clientGraphVessel[i])
			#print pid
			serverInd = find_ind(pid,serverGraph)
		
			if ((serverInd==-1) and (pid not in deletedShips)):
				print "created",pid
				#print deletedShips
				#print pid
				#print "hi"
				#not in server
				serverGraph.append(clientGraphVessel[i])
				shipVers[pid] = []#[client_address[0]]
			else:
				#if client is up to date:
				if client_address[0] in shipVers[pid]:
					#check if they are the same
					if compare_tree(clientGraphVessel[i], serverGraph[serverInd]):
						#print "yo"
						serverGraph[serverInd] = clientGraphVessel[i]
						shipVers[pid] = []#[client_address[0]]
				else:
					#because we're updating the client
					pass
					#shipVers[pid].append(client_address[0])
		#remove ships if client was up to date
		for x in serverGraph:
			if x not in clientGraphVessel and client_address[0] in shipVers[getPID(x)]:
				if delete:
					print "removed",getPID(x) 
					deletedShips.append(getPID(x))
					serverGraph.remove(x)
					shipVers[getPID(x)]=[]
					#print ""
					#print serverGraph
					#print ""
			else:
				shipVers[getPID(x)].append(client_address[0])

	
		print "Flightstate handled"
	
		#ROSTER
		for i in range(len(clientGraphKerbal)):
			name=get_name(clientGraphKerbal[i])
			serverInd = find_k_ind(name,kerbalGraph)
			if (serverInd==-1):
				#print "hi1"
				#not in server
				print "created",name
				kerbalGraph.append(clientGraphKerbal[i])
				shipVers[name] = [client_address[0]]
			else:
				#if client is up to date:
				if client_address[0] in shipVers[name]:
					#check if they are the same
					if compare_tree(clientGraphKerbal[i], kerbalGraph[serverInd]):
						#print "yo1"
						kerbalGraph[serverInd] = clientGraphKerbal[i]
						shipVers[name] = [client_address[0]]
				else:
					#because we're updating the client
					shipVers[name].append(client_address[0])
	
		print "Roster handled"
	
		#print clientGraphDestructablesReduced
	
		#print "\n\n\n"
		#Destructables
		for i in range(0,len(clientGraphDestructablesReduced),2):	
		
			code=clientGraphDestructablesReduced[i]
		
			serverInd = find_d_ind(code,destructGraph)
		
		
			if (serverInd==-1):
				#not in server
				destructGraph.append([code,clientGraphDestructablesReduced[i+1]])
				shipVers[code] = [client_address[0]]
			else:
				#if client is up to date:
				if client_address[0] in shipVers[code]:
					#check if they are the same
					if compare_tree([code,clientGraphDestructablesReduced[i+1]], destructGraph[serverInd]):
						#print "yo1"
						destructGraph[serverInd] = [code,clientGraphDestructablesReduced[i+1]]
						shipVers[code] = [client_address[0]]
				else:
					#because we're updating the client
					shipVers[code].append(client_address[0])
	
		sendDestruct = []
		for nod in destructGraph:
			sendDestruct.extend(nod)
		##destructGraphReduced=[]
		#print destructGraph
	
		##for i in range(len(destructGraph)):
		##	destructGraphReduced.append(destructGraph[i][0])
		
		##	print destructGraph[i]
		
		'''for i in range(len(clientGraphDestructablesReduced)):
			#name=get_name(clientGraphKerbal[i])
			serverInd = find_k_ind(name,kerbalGraph)
			if (serverInd==-1):
				#print "hi1"
				#not in server
				kerbalGraph.append(clientGraphKerbal[i])
				shipVers[name] = [client_address[0]]
			else:
				#if client is up to date:
				if client_address[0] in shipVers[name]:
					#check if they are the same
					if compare_tree(clientGraphKerbal[i], kerbalGraph[serverInd]):
						#print "yo1"
						kerbalGraph[serverInd] = clientGraphKerbal[i]
						shipVers[name] = [client_address[0]]
				else:
					#because we're updating the client
					shipVers[name].append(client_address[0])'''
	
		print "Destructables handled"
	
	
	
	#print serverGraph
	
	#this is where we send the stuff back
	print "sending data"
	returndata=(pickle.dumps((serverGraph,kerbalGraph,sendDestruct)))
	#print returndata
	connection.sendall(returndata)
	connection.sendall('abcdefg')
	print "data sent"

	saveData = open("serverSave.pkl", 'w')
	pickle.dump((serverGraph, kerbalGraph, sendDestruct, deletedShips, shipVers), saveData)
	saveData.close()
serversocket.close()
