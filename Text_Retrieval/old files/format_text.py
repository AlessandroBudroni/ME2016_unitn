import sys
import os
import string
import re
import file_navigator

rawDataPath = '/Users/alessandrobudroni/Dev/ME2016_unitn/Text_Retrieval/dataset'
dataPath = '/Users/alessandrobudroni/Dev/ME2016_unitn/Text_Retrieval/dataset'

for eventFolder in file_navigator.list_events(rawDataPath):
  print(eventFolder)
  for imageFolder in file_navigator.list_events(rawDataPath + eventFolder):
    print(imageFolder)
    for textFileName in file_navigator.list_events(rawDataPath + eventFolder + '/' + imageFolder):
      
      if not textFileName == 'links.txt':
        print('open %s' % textFileName)
        rawTextFile = open(rawDataPath + eventFolder + '/' + imageFolder + '/' + textFileName, 'r')
        rawText = rawTextFile.read()
        textSpaces = re.sub(r'\s+', ' ', rawText)
        text = re.sub(r'[^\x00-\x7F]+', ' ', textSpaces)
        textFile = open(dataPath + eventFolder + '/' + imageFolder + '/' + textFileName, 'w')
        textFile.write('%s' % text)
        rawTextFile.close()
        textFile.close()
      else:
        print('skipping Link file')
