#usr/bin/python
import socket
import cPickle as pickle
#import pickle
import sys
from kspLib import *


cfn = "settings.txt"

clientSettings = open(cfn)
fn = clientSettings.readline().strip()
loadData = open(fn)
ip = clientSettings.readline().strip()
port = int(clientSettings.readline().strip())
clientSettings.close()
fullData = loadData.read()
loadData.close()

#create an INET, STREAMing socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#now connect to the web server on port 80
# - the normal http port
s.connect((ip, port))

# Send data
s.sendall(fullData)
s.sendall('abcde')

totalData=""
'''while True:
	data = connection.recv(2048)
	if data:
		totaldata+=data
	else:
		break'''
	
totalData = s.recv(81920)

#print totaldata

print 'closing socket'
s.close()

print totalData

clientGraph = fillTree(fullData)
shipList = pickle.loads(totalData)
for i in range(len(shipList)):
	shipList.insert(i*2, "VESSEL")

vesselStr = unTree(shipList, 2)

upData = ''
dataStream = StringIO.StringIO(fullData)
for line in dataStream:
	if line == '\t\tVESSEL\n':
		for waste in dataStream:
			if waste == '\t}\n':
				upData += vesselStr
				upData += waste
				break
	upData += line
fullData = unTree(clientGraph)
writeFile = open(fn,"w")
writeFile.write(fullData);
writeFile.close()
