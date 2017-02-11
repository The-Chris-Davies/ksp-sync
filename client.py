import socket
import sys


#create an INET, STREAMing socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)




#now connect to the web server on port 80
# - the normal http port
s.connect(("pi.codexwilkes.com", 8988))



# Send data
message = 'This is the message.  It will be repeated.'
print >>sys.stderr, 'sending "%s"' % message
s.sendall(message)

# Look for the response
amount_received = 0
amount_expected = len(message)

while amount_received < amount_expected:
	data = s.recv(16)
	amount_received += len(data)
	print >>sys.stderr, 'received "%s"' % data

print >>sys.stderr, 'closing socket'
s.close()
