#import urllib2
#from urllib2 import urlopen
#from cookielib import CookieJar
#
#import time
## to avoid cookies
#cj = CookieJar()
#opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
#
#opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17')]
#
## paths
#filePath = '/Users/andreapilzer/Dropbox/Finali serie A/DSC_5185.JPG'
#searchUrl = 'https://www.google.com/searchbyimage/upload'
#
#sourceCode = opener.open(searchUrl)
import re
import urllib
import urllib2

filePath = '/Users/andreapilzer/Dropbox/Finali serie A/DSC_5185.JPG'

multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}
query_args = { 'q':'query string', 'foo':'bar' }

request = urllib2.Request('https://www.google.com/searchbyimage/upload')
print 'Request method before data:', request.get_method()

request.add_data(urllib.urlencode(multipart))
print 'Request method after data :', request.get_method()
request.add_header('User-agent', 'PyMOTW (http://www.doughellmann.com/PyMOTW/)')

print
print 'OUTGOING DATA:'
print request.get_data()

print
print 'SERVER RESPONSE:'
source = urllib2.urlopen(request).read()
print source

findLinks = re.findall(r'<div class="rg_meta">{"os":".*?","cb":.*?,"ou":"(.*?)","rh":"}',source)
for eachUrl in findLinks:
  print(eachUrl)


