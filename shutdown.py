import socket, sys

if(len(sys.argv) < 0) :
    print "Please enter a single number"
else :
    port = 8080
    host = 'localhost'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    s.settimeout(100.0)
    print("Connection established!")
    s.sendall("KILL_SERVICE\n")
    data = s.recv(1024)
    print 'Received ',data
    while 1: 
        s.sendall("Crap\n")
    s.close() #Close socket
