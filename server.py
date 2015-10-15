import socket, select, thread, mutex, sys
from threading import Thread, Lock
from Queue import Queue

online = True
shutdownLock = Lock()#Lock for online, used to shutdown server
IP_Address = socket.gethostbyname(socket.getfqdn())
port = 8080 #Default port
ID = "df7806c8c916f5e364762e23627f39fcebedca1221d080d0f8b96b0680e20bd2"
NUM_THREADS = 20
QUEUE_SIZE = NUM_THREADS*3

def stopWorker():
    return False
    
def setOnline(value) :
    global shutdownLock, online
    shutdownLock.acquire()
    try:
        online = value
    finally:
        shutdownLock.release()
        
def readOnline():
    global shutdownLock, online
    shutdownLock.acquire()
    result = True
    try:
        result = online
    finally:
        shutdownLock.release()
    return result

def handleClient(connection, address):
    global port, ID, IP_Address
    print 'Connected by ', address
    data = connection.recv(1024)
    keepRunning = True
    if(data == "KILL_SERVICE\n") :
        setOnline(False)
        keepRunning = False
    elif(str.startswith(data,"HELO ") and str.endswith(data,"\n")):
        connection.sendall(data + "IP:" + IP_Address+"\nPort:"+str(port)+"\nStudentID:"+ID+"\n")    
    else:
        #do nothing
        1+1
    return keepRunning

class Worker(Thread):
    def __init__(self, queue):
        self.tasks = queue
        self.on = True
        Thread.__init__(self)
        self.start()
        
    def run(self):
        while self.on:
            func, args, kargs = self.tasks.get()
            self.on = func(*args, **kargs)
        #     print "Done"
    
class ThreadPool: 
    def __init__(self, n, size):
        self.queue = Queue(size)
        self.num = n
        self.threads = []
        for i in range(0, n):
            self.threads.append(Worker(self.queue))
    def addTask(self, func, *args, **kargs):
        self.queue.put((func, args, kargs))
    
    def endThreads(self):
        for i in range(0, self.num):
            self.addTask(stopWorker)
        for i in range(0, self.num):
            self.threads[i].join()            
#        self.queue.join()



if(len(sys.argv) < 2) :
    print "Please enter a decimal number for the port e.g. server.py 5555"
else :    
    try: 
        port = int(sys.argv[1])
        if(len(sys.argv) > 2 ):
            NUM_THREADS = int(sys.argv[2])
            if(len(sys.argv) > 3):
                QUEUE_SIZE = int(sys.argv[3])            
        HOST = 'localhost'              #Start on localhoast
        pool = ThreadPool(NUM_THREADS, QUEUE_SIZE)   #Create Thread pool with queue size stated
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, port))
        try: 
            s.listen(1)
            list = [s]
            while readOnline():
                read, write, error = select.select(list, [], [], 0.1)
                for sock in read:
                    if(sock is s):            
                        c, a = sock.accept()
                        pool.addTask(handleClient, c,a)
            pool.endThreads()    
            s.close()
            print "Server shutting down..."
        except Exception, e:
            print e
        finally:
            s.close()
    except Exception, e:
        print e
        