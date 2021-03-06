# MAIN FUNCTION
# USES THE FILE_NAVIGATOR AND TEXT_RETRIEVAL FILES
# SAVES THE LINKS OF THE WEBPAGES
# SAVES THE TEXT IN TXT FILES NUMBERED FROM 1 TO THE NUMBER OF LINKS
# IF A NUMBER.TXT FILE IS MISSING THEN IT WAS A BAD LINK

import file_navigator
import link_retrieval2
import os
import sys
import urllib
import re
import string
from bs4 import BeautifulSoup
import time



# dataset
mainPath = 'dataset/'
# load folders in dataset
events = file_navigator.list_events(mainPath)

# choose the folders to search if you want to parallelize
#events = events[10:20]

exclude = set(string.punctuation)

def split_words(s):
  return re.sub(r"([a-z0-9\!?])([A-Z])", r"\1 \2", s)

def punct_cleaner(s):
  return ''.join(ch for ch in s if ch not in exclude)

def kill_newlines(s):
  s = re.sub(r'[^\x00-\x7F]+',' ', s)
  #s = re.sub(r" +", r" ", s)
  return re.sub(r"\n", r"", s)

# NAVIGATES ALL THE FOLDERS AND ALL THE IMAGES IN CHALEARN DATASET
for currEvent in events:
  print('--- FOR EVENT %s' % currEvent)
  images = file_navigator.list_events(mainPath+currEvent)
  if currEvent == 'Non-Class':
    images = [images[-1]]
  for currImage in images:
    start_time = time.time()
    if not ((".jpeg" in currImage) or (".jpg" in currImage) or (".png" in currImage) or (".gif" in currImage) or (".svg" in currImage)):
        continue
    print('--- FOR IMAGE %s' % currImage)
    links = link_retrieval2.find_related_links(mainPath + currEvent + '/' + currImage, 20)
    currImageName = file_navigator.extract_name(currImage)
    if not os.path.exists(mainPath+currEvent+'/'+currImageName):
      os.mkdir(mainPath+currEvent+'/'+currImageName)
    linkFile = open(mainPath+currEvent+'/'+currImageName+'/'+'links.txt','w')
    for url in links:
      linkFile.write('%s\n' % url)
    linkFile.close()

    # text extraction from related links and save

    numArticle = 1
    for url in links:
      print('FOR LOOP')
      try:
        html_page = urllib.urlopen(url).read()
        soup = BeautifulSoup(html_page,"lxml")

        for script in soup(["script", "style"]):
          script.extract()

        text = soup.body.get_text()
        textNewLine = kill_newlines(text)

        textNoPunct = punct_cleaner(textNewLine)
        textNoPunct = split_words(textNoPunct)
        textNoPunct = textNoPunct.lower()

        textNoPunct = re.sub(r" +", r" ", textNoPunct)
  
        text_file = open(mainPath+currEvent+'/'+currImageName+'/'+str(numArticle)+'.txt','w')
        text_file.write('%s' % textNoPunct)
        text_file.close()
        numArticle += 1

      except:
        print('Bad Link')
        numArticle += 1

    # measure running time of an image search
    print("--- %s seconds ---" % (time.time() - start_time))