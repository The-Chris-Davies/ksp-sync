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
#make backups
backups = open("backup.sfs", 'w')
backups.write(fullData)
backups.close()
loadData.close()

#create an INET, STREAMing socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#now connect to the web server on port 80
# - the normal http port
s.connect((ip, port))

# Send data
s.sendall(fullData)
s.sendall('abcdefg')

totalData=""
while True:
	data = s.recv(2048)
	totalData+=data
	if totalData[-7:]=="abcdefg":
		break
totalData=totalData[:-7]

print 'closing socket'
s.close()

datafromserver=pickle.loads(totalData)

shipList = datafromserver[0]
for i in range(len(shipList)):
	shipList.insert(i*2, "VESSEL")
vesselStr = unTree(shipList, 2)


kerbalList = datafromserver[1]
for i in range(len(kerbalList)):
	kerbalList.insert(i*2, "KERBAL")
kerbalStr = unTree(kerbalList, 2)



print vesselStr

upData = ''
dataStream = StringIO.StringIO(fullData)
for line in dataStream:
	if line == '\t\tVESSEL\n':
		for waste in dataStream:
			if waste == '\t}\n':
				upData += vesselStr
				upData += waste
				break
	elif line == '\t\tKERBAL\n':
		for waste in dataStream:
			if waste == '\t}\n':
				upData += kerbalStr
				upData += waste
				break
	else:
		upData += line


writeFile = open(fn,"w")
writeFile.write(upData);
writeFile.close()
