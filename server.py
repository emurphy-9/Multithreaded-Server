import socket, thread, math, time
from multiprocessing import Pool

def handleClient(connection, address):
    print 'Connected by ', address
    data = connection.recv(1024)
    x = math.sqrt(int(data))
    print "Square root of: ", data, "is: ", x
    connection.sendall(str(x))    

NUM_THREADS = 5
HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 8080              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

while True:
    thread.start_new_thread(handleClient, s.accept())
conn.close()