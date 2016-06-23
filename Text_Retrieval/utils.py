from urlparse import urlparse


# this function check if a link is good or not
def isAGoodLink(link):

  bad_sites = ['https://www.youtube.com', \
               'https://github.com', \
               'https://www.flickr.com', \
               'https://www.instagram.com', \
               'https://www.facebook.com', \
               'https://twitter.com', \
               'https://www.dropbox.com'
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


