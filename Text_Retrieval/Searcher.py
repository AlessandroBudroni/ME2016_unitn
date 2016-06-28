from GoogleScraper import scrape_with_config, GoogleSearchError
from GoogleScraper.database import ScraperSearch, SERP, Link

import utils

def searchongoogle(text, num):
    config = {
        'keyword': text,
        'use_own_ip': 'True',
        'num_results_per_page': 10,
        'num_pages_for_keyword': 2,
        'sel_browser': 'chrome',
        'do_caching': 'False',
        'scrape_method' : 'http'
    }
    try:
        sqlalchemy_session = scrape_with_config(config)
    except GoogleSearchError as e:
        print(e)

    linklist = []
    count = 0

    for i in range(1, len(sqlalchemy_session.serps ) + 1):
        s = []
        for ss in sqlalchemy_session.serps:
            if ss.page_number == i:
                s = ss
                break

        for link in s.links:
            l = str(link)[str(link).index('http'):str(link).__len__() - 1]
            if utils.isAGoodLink(l) and not linklist.__contains__(l):
                linklist.append(l)
                count += 1
                if count == num:
                    print('Founded ' + str(linklist.__len__()) + ' link on Google for: ' + text)
                    return linklist

    print('Founded ' + str(linklist.__len__()) + ' link on Google for: ' + text)
    return linklist
