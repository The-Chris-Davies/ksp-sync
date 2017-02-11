#usr/bin/python
import socket
import sys

loadData = open("persistent.sfs")

#create an INET, STREAMing socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#now connect to the web server on port 80
# - the normal http port
s.connect(("pi.codexwilkes.com", 8988))

# Send data
#message = 'This is the message.  It will be repeated.'
s.sendall(loadData)


while data!="end":
	data = s.recv(2048)
	#amount_received += len(data)
	#print >>sys.stderr, 'received "%s"' % data

print 'closing socket'
s.close()
