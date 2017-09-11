'''
Run a google search of business names in Companies House and return a wordcloud
of text from the first page of results

The code below builds up the code for functions that run searches and produce
worldclouds as follows:

cloud(keyWords(search('Company Name')))

search(string): returns a list of URLs from Google for the given term
keyWords(list): screen-scrapes all visible text from the given list of URLs, and cleans
cloud(string): after removing a given list of stopwords, produces a wordcloud

---
0) Modules & Prerequisites
'''

import pandas as pd
from pandas import DataFrame, Series
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import webbrowser #to open links
import nltk
from nltk.corpus import stopwords # Import the stop word list, may require download
# WordCloud modules
from wordcloud import WordCloud, STOPWORDS

# Increase figure and font sizes for easier viewing
plt.rcParams['figure.figsize'] = (8, 6)
plt.rcParams['font.size'] = 14

# Web-scraping modules
import re
from time import sleep
import requests
from bs4 import BeautifulSoup

#read cleaned up data from local directory
ch = pd.read_csv('ch_0917.csv')

'''
1) Building blocks to return links for a search term
'''

# Enter business search term here
biz = 'DYSON LIMITED'

# Read HTML
html = requests.get('https://www.google.co.uk/search?q='+biz)
# Parse HTML into a BeautifulSoup object
soup = BeautifulSoup(html.content, 'lxml')

# Get all links and put into list
links = []
for link in soup.find_all('a'):
    links.append(link.get('href'))

# Cleaning up results
links = DataFrame({'list':my_list}) #turn list into DF
links = links[links.list.str.contains('/url?')] #Only search results
# remove cached sites
links = links[links.list.str.contains('webcache.googleusercontent') == False]

# remove opening url?q= string and suffixed '&sa' bit
links = links.list.str.replace('/url\?q=',"")
#for some reason, after this, you don't need to call list anymore on the column

# remove suffixed &sa bit by splitting and drop index
links = links.str.split('&sa',1).reset_index().drop('index',1)
# this is now a dataframe

# use iterrows to grab first entry in each list which should be the working url
links2 = []
for row in links.iterrows():
    links2.append(row[1][0][0])

# convert to dataframe
links2 = DataFrame(links2)

'''
2) Function that takes in a search term and returns search links from Google
in a DataFrame
'''

def search(term):
    # Read HTML
    html = requests.get('https://www.google.co.uk/search?q='+term)
    # Parse HTML into a BeautifulSoup object
    soup = BeautifulSoup(html.content, 'lxml')

    # Get all links and put into list
    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))

    # Cleaning up results
    links = DataFrame({'list':links}) #turn list into DF
    links = links[links.list.str.contains('/url?')] #only search results
    # remove cached sites
    links = links[links.list.str.contains('webcache.googleusercontent') == False]

    # remove opening url?q= string and suffixed '&sa' bit
    links = links.list.str.replace('/url\?q=',"")
    #for some reason, after this, you don't need to call list anymore on /
    # the column

    # remove suffixed &sa bit by splitting and drop index
    links = links.str.split('&sa',1).reset_index().drop('index',1)
    # this is now a dataframe

    # use iterrows to grab first entry in each list which should be the working url
    links2 = []
    for row in links.iterrows():
        links2.append(row[1][0][0])
    # convert to dataframe
    links2 = DataFrame(links2)

    return links2[0]

# example of a search
dyson = search('DYSON LIMITED')

# open all links in browser
for link in dyson:
    webbrowser.open(link)

# TO-DO - REMOVE COMPANIES HOUSE AND OTHER LINKS FROM RESULTS

'''
3) Extract key text from company websites
Building blocks and helper functions
'''

#list of links
dyson = search('DYSON LIMITED')

# Read HTML
html = requests.get(dyson[0])
# Parse HTML into a BeautifulSoup object
soup = BeautifulSoup(html.content, 'lxml')

[s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]

visible_text = soup.getText().encode('ascii','ignore')

visible_text.replace('\n','').replace('\t','').replace('\r','')

# Use regular expressions to do a find-and-replace
def stripsymbols(text):
    x = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",text)
    x = re.sub('/(^|\b)@\S*($|\b)/'," ",x)
    x = re.sub('/(^|\b)#\S*($|\b)/'," ",x)
    x = re.sub("[^a-zA-Z]"," ",x)
    x = re.sub(r"(?:\@|https?\://)\S+", " ",x)
    return x

# Remove stop words from "words"
def removeStopWords(text):
    words = [w for w in text if not w in stopwords.words("english")]
    return words

# Print stopwords.words("english")

# Lambda function to rejoin list
#rejoin = lambda s: " ".join(s)

# Functions that cleans up HTML text and returns a list of words
def cleantext(text):
    # Remove stopwords and split text
    text.replace('\n','').replace('\t','').replace('\r','')
    splitList = stripsymbols(text.lower()).strip().split()
    return ' '.join(removeStopWords(splitList))


'''
4) Function that scrapes all visible text from a list of websites,
and cleans by removing stopwords, symbols etc. Another function to generate
a word cloud of these.
'''

#TO-DO - Do the following to get better key words:
    # store locator, blog, store, follow us, shop, etc.
    # Remove spacing variants
    # perhaps only select websites with at least one keyword?
    # Perhaps remove word within the search term itself?


def keyWords(list):
    words = ''
    for website in list:
        #try/except for troublesome websites
        try:
            html = requests.get(website)
            soup = BeautifulSoup(html.content, 'lxml')
            [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
            visibleText = soup.getText().encode('ascii','ignore')
            words += cleantext(visibleText)
        except:
            continue
    # Return list of words
    keywords = " ".join([word for word in words.split()
                                if 'http' not in word
                                    and not word.startswith('@')
                                    and word != 'RT'
                                if 'co' not in word
                                if word not in STOPWORDS
                                ])
    return keywords


def cloud(words):
    wordcloud = WordCloud(stopwords=STOPWORDS,
                          background_color='black',
                          width=1800,
                          height=1400
                         ).generate(words)

    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()
    return wordcloud


'''
5) Examples
'''

cloud(keyWords(search('Dyson Limited')))
cloud(keyWords(search('Royal Bank of Scotland')))
cloud(keyWords(search('News Corporation')))

'''
6) Example: sample of 10 companies for 7100: mining of iron ores
'''

ch7100 = ch[ch.sic1.str.contains('7100 - Mining of iron ores')]
# Get a random sample of 10
ch7100s = ch7100.sample(10)

text = ''
for company in ch7100s.name:
    text += keyWords(search(company))
    sleep(np.random.randint(10,30))

wordcloud = WordCloud(
                    stopwords=STOPWORDS,
                    background_color='black',
                    width=1800,
                    height=1400
                    ).generate(text)

plt.imshow(wordcloud)
plt.axis('off')
plt.show()

'''
7) Extend STOPWORDS list to remove certain words
'''

STOPWORDS.add(['sun','new','showbiz','tv','uk'])
