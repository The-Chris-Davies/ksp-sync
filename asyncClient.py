#usr/bin/python
import socket
import cPickle as pickle
import sys
from kspLib import *

fn = "persistent.sfs"
cfn = "settings.txt"

loadData = open(fn)

clientSettings = open(cfn)
ip = clientSettings.readline().strip()
port = int(clientSettings.readline().strip())
clientSettings.close()
fullData = loadData.read()
loadData.close()
'''
#create an INET, STREAMing socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#now connect to the web server on port 80
# - the normal http port
s.connect((ip, 8988))

# Send data
#message = 'This is the message.  It will be repeated.'
s.sendall(fullData)

totalData=""
while True:
	data = s.recv(2048)
	if data=="end":
		totalData += data
	#DO SOMETHING WITH RECIEVED DATA.

print 'closing socket'
s.close()
'''
#shipList = pickle.loads(totalData)
shipList = [['kill'],['me']]
for i in range(len(shipList)):
	shipList.insert(i*2, "VESSEL")

vesselStr = unTree(shipList, 2)
#print vesselStr

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
print upData
#print clientGraph
#fullData = unTree(clientGraph)
#writeFile = open(fn,"w")
#writeFile.write(fullData);
#writeFile.close()
