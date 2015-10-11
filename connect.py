import socket, sys

if(len(sys.argv) != 2) :
    print "Please enter a single number"
else :
    port = 8080
    host = 'localhost'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    print("Connection established!")
    s.sendall(sys.argv[1])
    print "Messages sent"
    data = s.recv(1024)
    s.close() #Close socket
    print 'Received ',data
