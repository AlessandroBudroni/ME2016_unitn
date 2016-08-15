from urllib.parse import urlparse


# this function checks if a link is good or not
def isAGoodLink(link):

  bad_sites = ['https://www.youtube.com', \
               'http://m.youtube.com', \
               'https://m.youtube.com', \
               'https://github.com', \
               'https://www.flickr.com', \
               'https://www.instagram.com', \
               'https://www.facebook.com', \
               'https://twitter.com', \
               'https://www.dropbox.com', \
               'https://nytimes.com',\
               'http://nytimes.com', \
               'http://www.nytimes.com', \
               'http://www.nytimes.com', \
               'http://mobile.nytimes.com',\
               'http://www.mobile.nytimes.com',\
               'https://plus.google.com'
               ]
  bad_extensions = ['.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx', '.csv','.ps']

  o = urlparse(link)

  matching = [s for s in bad_sites if urlparse(s).netloc == o.netloc]
  if len(matching) > 0:
      return 0

  matching = [e for e in bad_extensions if link.find(e) > -1]
  if len(matching) > 0:
      return 0

  return 1


