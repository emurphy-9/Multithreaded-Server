# Multithreaded-Server
Distributed Systems Multithreaded Server
Lab2

Name: Eoin Murphy
Student ID: df7806c8c916f5e364762e23627f39fcebedca1221d080d0f8b96b0680e20bd2

<<<<<<< HEAD
Solution written in Python, Thread Pooling implemented in server not taken from a library.

The sever takes in a number of command line arguments, the port number is mandatory all others are optional

Args: server.py <PORT NUMBER> <DEBUG> <NUMBER OF THREADS> <SIZE OF QUEUE>

The Port Number determines which port the server will run on

Debug determines if debug information is printed out (currently just message contents), set to 0 for no debug info, otherwise set to any other number (typically 1)

Number of Threads determines the number of threads in the thread pool

Size of queue determines the size of the queue for the thread pool, it sets how many tasks can be in the queue. This effectively caps the number of socket connections that can be kept on hold, all others will be ignored.
=======
Solution written in Python, Thread Pooling implemented in server (not taken from a library).
>>>>>>> origin/master
