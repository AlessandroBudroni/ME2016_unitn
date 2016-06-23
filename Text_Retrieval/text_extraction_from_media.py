import file_navigator
import link_retrieval
import os
import sys
import urllib
import re
import string
from bs4 import BeautifulSoup
import time
import csv
import sqlite3

# BEGIN FUNCTION DECLARATIONS

# This function gets text from a webpage
def getTextFromLink(l):
    try:
        html_page = urllib.urlopen(l).read()
        soup = BeautifulSoup(html_page, "lxml")

        # removing all scripts and stype tags
        for script in soup(["script", "style", "a", "href"]):
            script.extract()

        # get the body part
        text = soup.body.get_text()

        return text

    except:
        return 'Bad Link'


# This function get text from a Youtube link
# There are some cases in which the videos come from Dropbox. We ignore these exceptions
def getTextFromVideoLink(l):
    try:
        html_page = urllib.urlopen(l).read()
        soup = BeautifulSoup(html_page, "lxml")

        # removing all scripts and stype tags
        for script in soup(["script", "style", "a", "href"]):
            script.extract()

        # get the body part
        text = soup.title.get_text()
        text = text + ' ' + soup.find(id="watch-description").get_text()

        return text

    except:
        return 'Bad Link'


# END FUNCTION DECLARATION









# BEGIN MAIN SCRIPT

# some definitions
nPages = 20

#development set - multimedia details
output_dir = 'dataset/devset'
multimedia_dev_details = output_dir + '/multimedia_dev_details.csv'

# store data to dev.db
db_file = os.path.join(output_dir, 'dev.db')

# for debugging, remove file if existed
useExistingDB = 0 # assign to 1 if wanna use the existing DB

if useExistingDB == 0 and os.path.isfile(db_file):
    os.remove(db_file)

# connect to database
conn = sqlite3.connect(db_file)
c = conn.cursor()

# Create table if needed
if useExistingDB == 0:
    c.execute('''CREATE TABLE website_from_img
             (mul_id text, page_url text, body text)''')

# for resuming ^ ^
running_from = 1;
running_to = 5;

count = 0;

with open(multimedia_dev_details) as csvfileDetail:
    reader = csv.DictReader(csvfileDetail)

    #read row by csvfileDetails
    for row in reader:
        mul_id = row['mul_id']
        type = row['type']
        event_name = row['event_name']
        abs_path = row['abs_path']

        # for resuming ^ ^
        count = count + 1
        if count < running_from:
            continue
        if count > running_to:
            break

        print('Processing mm ' + str(count) + ': ' + mul_id)

        # retrieve data and save in SQLite
        data = []

        if type == 'image':
            links = link_retrieval.find_related_links(abs_path, nPages)

            for l in links:
                text = getTextFromLink(l)
                print("===>" + l)
                # accumulate data
                data.append((mul_id, l, text))

        if type == 'video':
            print("===>" + abs_path)
            text = getTextFromLink(abs_path)
            # accumulate data
            data.append((mul_id, abs_path, text))

        # insert data into database
        c.executemany("INSERT INTO website_from_img VALUES (?,?,?)", data)
        conn.commit()

# disconnect from DB
conn.close()

# close *.csv
csvfileDetail.close()

# END MAIN SCRIPT