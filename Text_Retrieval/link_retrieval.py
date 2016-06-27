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
import urlparse as urlparse
# cookies
import cookielib
from bs4 import BeautifulSoup
import utils as utils

# this function returns 'num' links related to the image (path)

def find_related_links(path, num=10):
  # controlla perche non so se fa qualcosa davvero

  cj = cookielib.CookieJar()

  # custom opener
  host = 'https://www.google.com/'
  searchUrl = 'https://www.google.com/searchbyimage/upload'

  multipart = {'encoded_image': (path, open(path, 'rb')), 'image_content': ''}

  # send request

  response = requests.post(searchUrl, files=multipart, allow_redirects = False)
  cj = requests.utils.cookiejar_from_dict(response.cookies.get_dict())
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
  opener.addheaders = [('User-agent',
                        'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17')]

  fetchUrl = response.headers['Location']

  nGoodLinks = 0
  links = []
  source = opener.open(fetchUrl).read()
  soup = BeautifulSoup(source)
  nextFetchUrl = ''
  while nGoodLinks < num:

    # navigate to the first page of results
    # only select relevant links (their parent has class 'r')
    anchors = soup.findAll('a')

    for an in anchors:
      parent = an.parent
      cl = parent.attrs.get('class')
      if cl == ['r']:
         #print(an.attrs.get('href'))
        l = an.attrs.get('href')
        if utils.isAGoodLink(l):
          links.append(l)
          nGoodLinks = nGoodLinks + 1

      # if not enough good links, navigate to next page
      cl = an.attrs.get('class')
      label = an.attrs.get('aria-label')
      if label != None and label.find('Page') != -1 and nextFetchUrl == '':
        nextFetchUrl = host + an.attrs.get('href')

    # enough good links, cut it off at num
    if nGoodLinks >= num:
      links = links[:num]
      break
    else:
      source = opener.open(nextFetchUrl).read()
      soup = BeautifulSoup(source)
      nextFetchUrl = ''

  return links


