# RETURNS THE LINKS OF THE WEBPAGES WHERE THE IMAGES ARE
# THE IMAGES ARE THE SIMILAR IMAGES RETURNED BY GOOGLE IMAGE SEARCH

# web browser call handler
import webbrowser
# python sftp
import pysftp as sftp
# regular expression to cut off image links
import re
# requests library that includes urllib2
import requests
import urllib2
# cookies
from cookielib import CookieJar


def find_related_images(path):
# controlla perche non so se fa qualcosa davvero
  cj = CookieJar()
  requests.utils.dict_from_cookiejar(cj)

  # custom opener
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
  opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17')]
  
  searchUrl = 'https://www.google.com/searchbyimage/upload'
  
  multipart = {'encoded_image': (path, open(path, 'rb')), 'image_content': ''}

  # send request
  response = requests.post(searchUrl, files=multipart, allow_redirects = False)
  fetchUrl = response.headers['Location']

  source = opener.open(fetchUrl).read()

  links = re.findall('"ou":"(.*?)","ow"', source)
  return links
