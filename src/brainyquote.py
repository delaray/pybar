#********************************************************************************
# Brainy Scraping Tools
#********************************************************************************


# Python imports
import os
from datetime import datetime
from bs4 import BeautifulSoup, SoupStrainer
import pandas as pd

# Project imports
from src.utils import make_data_pathname
from src.utils import tokenize_text
from src.scraper import get_url_response
from src.scraper import get_url_data

#--------------------------------------------------------------------
# Basic Tools
#--------------------------------------------------------------------

def get_brainyquote_url(topic, page):
    base_page = 'https://www.brainyquote.com/topics/' + topic + '-quotes'
    if page==0:
        return base_page
    else:
        return base_page + "_" + str(page)

#--------------------------------------------------------------------

def ensure_response(topic, url=None, response=None):
    if response is None:
        if url is None:
            url = get_brainyquote_url(topic)
        response = get_url_response(url)
        if response.status_code==200:
            return response
        else:
            return None
    else:
        return response

#--------------------------------------------------------------------

def get_topic_quotes(topic, response=None, limit=50):
    count = 0
    url = get_brainyquote_url(topic, count)
    response = ensure_response(topic, url=url)
    
    # Use a dictionary to ensure unique quotes.
    results = {}
    print ('Processing quotes for topic: ' + topic)

    # Iterate over all BrainyQuote pages.
    while response is not None and count < limit:
        print ('Processing page ' + str(count+1) + "...")
        soup = BeautifulSoup(response.content, 'lxml')
        divs = soup.find_all('div', {'class' : 'clearfix'})
        for entry in divs:
            atags = entry.find_all('a')
            if len(atags)==2:
                q = atags[0].text
                a = atags[1].text
                results.update({q : a})
            elif len(atags)==3:
                q = atags[1].text
                a = atags[2].text
                results.update({q : a})
        count += 1
        url = get_brainyquote_url(topic, count)
        response = ensure_response(topic, url=url)
        
    # Now place results in a DF
    rows = []
    source = 'BrainyQuote'
    url = 'https://www.brainyquote.com'
    for key, value in results.items():
        row = [value, key, topic, source, url, datetime.now()]
        rows.append(row)
    cols = ['author', 'quote', 'topic', 'source', 'source_url', 'created_on']
    # Return the dataframe.
    return pd.DataFrame(rows, columns=cols)
    

#--------------------------------------------------------------------
# Soup select examples
#--------------------------------------------------------------------

# atags = soup.select('a[href*="/quotes/"]')
# atags = [x for x in atags if x.next_element != '\n']

#--------------------------------------------------------------------
# End of File
#--------------------------------------------------------------------
