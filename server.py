import socket
import sys



#create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#bind the socket to a public host,
# and a well-known port
serversocket.bind((socket.gethostname(), 8988))
#become a server socket
serversocket.listen(5)

while 1:
	#accept connections from outside
	connection, client_address = serversocket.accept()
	
	print >>sys.stderr, 'connection from', client_address

	# Receive the data in small chunks and retransmit it
	while True:
		data = connection.recv(2048)
		print >>sys.stderr, 'received "%s"' % data
		if data:
			print >>sys.stderr, 'sending data back to the client'
			connection.sendall(data)
		else:
			print >>sys.stderr, 'no more data from', client_address
			break
	
