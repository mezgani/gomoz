import socket
import sys
import threading, Queue

MAX_THREADS = 150

class Scanner(threading.Thread):
    def __init__(self, src, dsc):
        threading.Thread.__init__(self)
        #self.setDaemon(1)
        # queues for (host, port)
        self.inpipe = src
        self.outpipe = dsc

    def run(self):
        while 1:
            host, port = self.inpipe.get()
            sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
            try:
                # connect to the given host:port
                sd.connect((host, port))
                sd.settimeout(1)
                #data=sd.recv(128)
              
                
            except socket.error:
                # set the CLOSED flag
                self.outpipe.put((host, port, 'CLOSED'))

            else:
                
                self.outpipe.put((host, port, 'open'))
                sd.close()


def scan(host, start, stop, nthreads):
    if nthreads is None or nthreads =='':
        nthreads = MAX_THREADS
    toscann = Queue.Queue()
    scanned = Queue.Queue()

    
    scanners = [Scanner(toscann, scanned) for i in range(nthreads)]
    for scanner in scanners:
        scanner.start()

    hostports = [(host, port) for port in xrange(start, stop+1)]
    for hostport in hostports:
        toscann.put(hostport)

    results = {}
    response={}
    for host, port in hostports:
        while (host, port) not in results:
            nhost, nport, nstatus = scanned.get()
            results[(nhost, nport)] = nstatus
        status = results[(host, port)]
        if status <> 'CLOSED':
            response[port]=status
    return response




class ScanOne:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def GetResult(self):
        socket.setdefaulttimeout(2)
        try:	
            sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.connect((self.host, self.port))
                sock.settimeout(100)
                return ("open") 
            except socket.error, reason:
                erno, error=reason
                return ("close")
        except :
            pass	
        
        finally:
            sock.close()
		
