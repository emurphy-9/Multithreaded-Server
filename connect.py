import socket, sys

if(len(sys.argv) < 0) :
    print "Please enter a single number"
else :
    port = 8080
    host = 'localhost'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    s.settimeout(1.0)
    
    print("Connection established!")
    s.sendall("HELO I AM A BT LOL :-)\n")
    data = s.recv(1024)
    print 'Received ',data
    s.close() #Close socket
