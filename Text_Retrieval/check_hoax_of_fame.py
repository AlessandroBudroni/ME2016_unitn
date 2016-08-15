import csv
import urllib
from bs4 import BeautifulSoup

event_testset_details = '/Users/quoctin/Documents/UNITN - No Dropbox/MediaEVAL/ME2016_unitn/Text_Retrieval/dataset/testset/multimedia_details.csv'

def getResultFromHOF(l):
    try:
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/601.2.7 (KHTML, like Gecko) Version/9.0.1 Safari/601.2.7')]
        html_page = opener.open(l).read()

        soup = BeautifulSoup(html_page, "lxml")

        anchors = soup.findAll('p')

        for an in anchors:
            parent = an.parent
            cl = parent.attrs.get('class')
            if cl == ['caption']:
                return an.text

        return None

    except:
        return None

def check_hoax_of_fame(event_name):

    event_name = event_name.replace('_', '+')

    search_link = 'http://hoaxoffame.tumblr.com/search/'+event_name
    result = getResultFromHOF(search_link)

    explanation = None
    p = [0,0]
    if result != None:
        if result.find('Yes') != -1:
            p[0] = 1
            explanation = search_link
        if result.find('No') != -1:
            p[1] = 1
            explanation = search_link
    return p,explanation
