import socket, select, thread, math, sys
from threading import Thread
from Queue import Queue

online = True

def stopWorker():
    return False

def handleClient(connection, address):
    print 'Connected by ', address
    data = connection.recv(1024)
    if(data == "KILL_SERVICE\n") :
        return False
    elif(str.startswith(data,"HELO ") and str.endswith(data,"\n")):
        connection.sendall(data + "IP:")    
    else:
        #do nothing
        1+1
    return True   

class Worker(Thread):
    def __init__(self, queue):
        self.tasks = queue
        self.on = True
        Thread.__init__(self)
        self.start()
        
    def run(self):
        global online
        while self.on:
            func, args, kargs = self.tasks.get()
            self.on = func(*args, **kargs)
        online = False
        #     print "Done"
    
class ThreadPool: 
    def __init__(self, n):
        self.queue = Queue()
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



if(len(sys.argv) != 2) :
    print "Please enter a single number"
else :    
    try: 
        port = int(sys.argv[1])
        print "IP address: ", socket.gethostbyname(socket.getfqdn()) 
        NUM_THREADS = 5
        HOST = ''                 # Symbolic name meaning all available interfaces
        pool = ThreadPool(NUM_THREADS)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, port))
        s.listen(1)
        list = [s]
        while online:
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
        