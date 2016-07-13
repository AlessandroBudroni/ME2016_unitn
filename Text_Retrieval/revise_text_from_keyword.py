import os
import sys
import csv
import sqlite3
import Searcher as searcher
import time
import urllib
from bs4 import BeautifulSoup

# BEGIN FUNCTION DECLARATIONS

# This function gets text from a webpage
def getTextFromLink(l):
    try:
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/601.2.7 (KHTML, like Gecko) Version/9.0.1 Safari/601.2.7')]
        html_page = opener.open(l).read()

        soup = BeautifulSoup(html_page, "lxml")

        # removing all scripts and stype tags
        for script in soup(["script", "style", "a", "href"]):
            script.extract()

        # get the body part
        text = soup.text

        return text

    except:
        return 'Bad Link'


#development set - multimedia details
output_dir = 'dataset/devset'
event_dev_details = output_dir + '/event_related_keywords.csv'

# store data to dev.db
db_file = os.path.join(output_dir, 'dev.db')

# for debugging, remove file if existed
useExistingDB = 1 # assign to 1 if wanna use the existing DB

if useExistingDB == 0 and os.path.isfile(db_file):
    os.remove(db_file)

# connect to database
conn = sqlite3.connect(db_file)
c = conn.cursor()

res = c.execute('SELECT * FROM website_from_keywords')

for row in res:
    if row[2] != 'Bad Link':
        continue
    text = getTextFromLink(row[1])
    print('process: ',row[0], '-', row[1])
    data = [(row[0], row[1], text)]
    c.execute("UPDATE website_from_keywords SET body = ? WHERE event_name = ? and page_url = ?", text, row[0], row[1])
    conn.commit()

conn.close()