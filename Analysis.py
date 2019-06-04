import Scraper
import pickle
from textblob import TextBlob


def sentiments(corpus):
    '''
    Get average sentiment of a list of strings, or "documents"
    Returns list of polarity (how positive/negative it is)
    and subjectivity (how biased it is)

    DOES NOT CALCULATE AVERAGE/MEDIAN/MODE
    '''

    polarity = []
    subjectivity = []

    for doc in corpus:
        docBlob = TextBlob(doc)
        polarity.append(docBlob.sentiment.polarity)
        subjectivity.append(docBlob.sentiment.subjectivity)

    return polarity, subjectivity


def sentimentTitles(oneStock):
    corpus = oneStock.titles
    return sentiments(corpus)

def sentimentSummaries(oneStock):
    corpus = oneStock.summaries
    return sentiments(corpus)

def sentimentNewsText(oneStock):
    corpus = oneStock.texts
    return sentiments(corpus)

def sentimentWikiReferences(oneStock):
    corpus = oneStock.wikiReferences
    return sentiments(corpus)

def sentimentWikiLinks(oneStock):
    corpus = oneStock.sentimentWikiLinks
    return sentiments(corpus)

def sentimentWikiSummary(oneStock):
    corpus = oneStock.wikiSummary
    return sentiments(corpus)

def sentimentWikiContent(oneStock):
    corpus = [oneStock.wikiContent]
    return sentiments(corpus)

def articleSentiments(stockList):
    '''
    The sentiment values come in an array over time
    Sometimes they're reversed, so we need to reverse them to correct
    '''

    #arrays of arrays
    titlePolarities = []
    titleBias = []
    textPolarities = []
    textBias = []

    for oneStock in stockList:

        titlePolarity, titleSubj = sentimentTitles(oneStock)
        titlePolarities.append(titlePolarity)
        titleBias.append(titleSubj)

        textPolarity, textSubj = sentimentNewsText(oneStock)
        textPolarities.append(textPolarity)
        textBias.append(textSubj)

    return titlePolarities, titleBias, textPolarities, textBias