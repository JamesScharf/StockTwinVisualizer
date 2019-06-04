import pandas as pd
import feedparser
from urllib import parse, request
import requests
from bs4 import BeautifulSoup
import wikipedia
import pickle
import datetime
import copy
import random 

def buildCompanyRSS(stock):
    '''
    Build RSS Feeds for a company
    '''
    return f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={stock}&region=US&lang=en-US"

def readPaper(rssFeed):
    '''
    Input website as list and a stock symbol (like APPL or GOOG) as a string
    and then return the news articles about this stock.
    '''
    feed = feedparser.parse(rssFeed)
    entries = feed["entries"]
    titles = []
    summaries = []
    texts = []
    for e in entries:

        try:

            r = requests.get(e['link'])
            html = r.text

            soup = BeautifulSoup(html, features="lxml")

            tags = soup.find_all('p')

            articleText = ""
            for tag in tags:
                if "{" not in tag.getText():
                    articleText += " " + tag.getText()
            #documents.append(NewsDocument(e["title"], e["summary"], articleText, e["published_parsed"]))
            titles.append(e["title"])
            summaries.append(e["summary"])
            texts.append(articleText)

        except:
            continue

    return titles, summaries, texts

class Stock:
    def __init__(self, symbol, name, industry):
        self.name = name
        self.symbol = symbol
        self.titles, self.summaries, self.texts = readPaper(buildCompanyRSS(symbol)) #one corpus
        try:
            wikiPage = wikipedia.page(name)
            if len(wikiPage.references) > 4:
                randReferences = random.sample(wikiPage.references, 4)
            else:
                randReferences = wikiPage.references
            self.wikiReferences = [scrapeReference(link) for link in randReferences] #text of references
            self.wikiLinks = wikiPage.links #don't run similarity metric -- just see how many links are shared between stock
            self.wikiSummary = wikiPage.summary
            self.wikiContent = wikiPage.content

        except:
            self.wikiReferences = []
            self.wikiLinks = []
            self.wikiSummary = ""
            self.wikiContent = ""

        self.industry = industry
        self.dateCreated = datetime.datetime.now()


def scrapeReference(link):
    '''
    Scrape the link of a wikipedia page
    '''
    try:
        r = requests.get(link)
        html = r.text

        soup = BeautifulSoup(html, features="lxml")

        tags = soup.find_all('p')   
        
        articleText = ""
        for tag in tags:
            if "{" not in tag.getText():
                articleText += " " + tag.getText()
    except:
        return ""
    
    return articleText

def scrape(sampleSize):
    companyList = pd.read_csv("companylist.csv")
    sampleStocks = companyList.sample(n = sampleSize)

    stockList = []
    for index, row in sampleStocks.iterrows():

        tempStock = Stock(row[0], row[1], row[7])
        stockList.append(tempStock)

    pickle.dump(stockList, open('stocks.p', 'wb'))    
    return stockList