import httplib, urllib2

class WebConnection:
    def __init__(self, host, path):
        self.host = host
        self.path = path
    def __report_header__(self):
        """ make a http HEAD request """
        try:
            h = httplib.HTTP(self.host) 
            h.putrequest("HEAD", "/"+self.path.strip("\n")) 
            h.putheader("Host", self.host)
            h.putheader('User-agent', 'python-httplib')
            h.endheaders() 
            status, reason, headers, server = h.getreply() 
            print "[+]",self.host+"/"+self.path.strip("\n"),":",status, reason 
        except: 
            #print "[-] Error Occurred" 
            pass




    def __report_url_header__(self):
        """ return a dictionary of a http HEAD request """
        request = urllib2.Request('http://'+self.host+'/')
        opener = urllib2.build_opener()
        f = opener.open(request)
        return f.headers.dict


def getinfo(ip):
    """return a dico of headers items"""
    c = WebConnection(ip,'/')
    c.__report_header__()
    data=c.__report_url_header__()
    return data

##if __name__=='__main__':
##    getinfo('127.0.0.1')
