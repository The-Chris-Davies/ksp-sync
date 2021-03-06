#usr/bin/python
import socket
import cPickle as pickle
#import pickle
import sys
from kspLib import *

if '-h'in sys.argv or '--help' in sys.argv:
	print """
	arguments:

	-h or --help:
		prints this message

	-r or --revert:
		downloads the current server data, effectively setting the client to the server's current save file.

	-nd or --nodelete:
		updates, signalling the server not to delete any missing ships. 
		In a perfect world, this wouldn't be necessary, but...
	"""
	sys.exit()


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

print "connected to socket"
# Send data

#	1 = download only	2 = delete mode is DISABLED
if '-r'in sys.argv or '--revert' in sys.argv:
	s.sendall('1')
elif '-nd' in sys.argv or '--nodelete' in sys.argv:
	s.sendall('2')
else:
	s.sendall("0")
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


destructStr = unTree(datafromserver[2], 2)

upData = ''
dataStream = StringIO.StringIO(fullData)
for line in dataStream:
	if line.strip().split()[0] == 'UT':
		upData += '\t\tUT = ' + str(datafromserver[3]) + '\n'
	elif line == '\t\tVESSEL\n':
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
	elif line == '\t\tname = ScenarioDestructibles\n':
		upData += line
		upData += dataStream.readline()
		for waste in dataStream:
			if waste == '\t}\n':
				upData += destructStr
				upData += waste
				break
	else:
		upData += line


writeFile = open(fn,"w")
writeFile.write(upData);
writeFile.close()

print "Success"
