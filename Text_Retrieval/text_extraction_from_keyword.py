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

        # get text
        text = soup.text

        return text

    except:
        return 'Bad Link'



# BEGIN MAIN SCRIPT

# some definitions
nPages = 10

#development set - multimedia details
output_dir = 'dataset/testset_subtask'
event_dev_details = output_dir + '/event_related_keywords.csv'

# store data to dev.db
db_file = os.path.join(output_dir, 'text_from_keywords.db')

# for debugging, remove file if existed
useExistingDB = 1 # assign to 1 if wanna use the existing DB

if useExistingDB == 0 and os.path.isfile(db_file):
    os.remove(db_file)

# connect to database
conn = sqlite3.connect(db_file)
c = conn.cursor()

# Create table if needed
if useExistingDB == 0:
    c.execute('''CREATE TABLE website_from_keywords
             (event text, page_url text, body text)''')

res = c.execute('SELECT * FROM website_from_keywords')

# for resuming ^ ^
running_from = 1
running_to = 1


with open(event_dev_details) as csvfileDetail:
    reader = csv.DictReader(csvfileDetail)
    # read row by csvfileDetails
    count = 0
    for row in reader:
        count += 1
        if count < running_from:
            continue
        if count > running_to:
            break


        keywords = row['keywords'].strip('\n\t ')
        event_name = row['event_name'].strip('\n\t ')
        print('processing ', count, ':', keywords)

        links = searcher.searchongoogle(keywords, nPages)

        data = []
        for l in links:
            text = getTextFromLink(l)
            print("===>" + l)
            # accumulate data
            data.append((event_name, l, text))

        # insert data into database
        c.executemany("INSERT INTO website_from_keywords VALUES (?,?,?)", data)
        conn.commit()

        #please google
        time.sleep(45)

conn.close()