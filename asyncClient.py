#usr/bin/python
import socket
import sys

fn = "persistent.sfs"
cfn = "clientSettings.txt"

loadData = open(fn)

clientSettings = open(cfn)
ip = clientSettings.readline().strip()
clientSettings.close()
#create an INET, STREAMing socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#now connect to the web server on port 80
# - the normal http port
s.connect((ip, 8988))

# Send data
#message = 'This is the message.  It will be repeated.'
s.sendall(loadData.read())

loadData.close()

totalData=""
while True:
	data = s.recv(2048)
	if data=="end":
		totalData += data
	#DO SOMETHING WITH RECIEVED DATA.

print 'closing socket'
s.close()


writeFile = open(fn,"w")
writeFile.write(totalData);
writeFile.close()