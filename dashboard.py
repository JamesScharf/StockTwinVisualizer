from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.layouts import column
from bokeh.layouts import row
from bokeh.models.widgets import Select, Paragraph
from bokeh.embed import components
import pandas as pd
import numpy as np

import statistics
from sklearn import decomposition
import Scraper
import compare
import Analysis
import pickle
from bokeh.layouts import gridplot





def barPlot(compareData, toCompare):
    '''
    toCompare is the column that we're comparing
    compareData is the data that comes from output.csv
    '''

    xBarNames = compareData["stock_SYMBOL"] #the things that we're listing
    counts = compareData[toCompare]

    p = figure(x_range=xBarNames, title= toCompare.replace("_", " "),
            toolbar_location="right", tools="pan,wheel_zoom,box_zoom,save", height = 300, sizing_mode='scale_width')

    p.vbar(x=xBarNames, top=counts, width=0.9)
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    
    return p

def relevanceDashboard(compareData):
    '''
    The dashboard for presenting stock
    similarity by corpuses.
    '''
    
    wikiPlot = barPlot(compareData, "WIKI_SIMILARITY")
    newsPlot = barPlot(compareData, "NEWS_SIMILARITY")
    linkSim = barPlot(compareData, "LINK_SIMILARITY")
    refSim = barPlot(compareData, "REFERENCE SIMILARITY")

    return components(gridplot([[wikiPlot, newsPlot], [linkSim, refSim]]))
    


def PCA(compareData):
    '''
    Take all the values and make a fancy plot showing similarity
    Which is ultimately meaningless but people like it
    '''

    X = compareData.loc["WIKI_SIMILARITY":]
    pca = decomposition.PCA(n_components=2)
    return pca.fit_transform(X)





def polarityDashboard(origStock, stockList, compareData):
    '''
    Make a dashboard for the news polarity stuff
    Output it to polarityDashboard.html
    '''
    
    #relevanceBar = barPlot(compareData, "NEWS_SIMILARITY")

    titlePolarities, titleBias, textPolarities, textBias = Analysis.articleSentiments(stockList)

    allFigures = []
    #allFigures.append([relevanceBar])
    #para = Paragraph(text="On this dashboard, you can see the polarity of relevant news articles and headlines. Strongly positive or negative headlines will drive short-term volatility, whereas the polarity of articles impact long-term growth.")

    
    #get averages of each
    means = []
    for oneStockTitles, oneStockTexts in zip(titlePolarities, textPolarities):
        if len(oneStockTitles) > 0 and len(oneStockTexts) > 0:
            means.append((statistics.mean(oneStockTitles) + statistics.mean(oneStockTexts)) / 2.0)

    if len(means) > 0:
        xBarNames = compareData["stock_SYMBOL"] #the things that we're listing
        polBar = figure(x_range=xBarNames, title= "Polarity Summary", y_axis_label='Polarity', height = 300, sizing_mode='scale_width')
        polBar.vbar(x=xBarNames, top=means, width=0.9)
    
        allFigures.append([polBar])
    colors = ["blue", "green", "orange", "purple", "magenta", "cyan", "yellow"]
    count = 1

    for oneStock, stockTitles in zip(stockList, titlePolarities):
        titleLen = list(range(1, len(stockTitles) + 1))
        polarityFigure = figure(title=f"{oneStock.name} Headline Polarity", x_axis_label='Time', y_axis_label='Polarity', height = 300, sizing_mode='scale_width')
        polarityFigure.line(x=titleLen, y=stockTitles, legend=oneStock.symbol, line_width=2, color=colors[count])

        if len(allFigures) - 1 > 0 and len(allFigures[len(allFigures) - 1]) >= 2:
            allFigures.append([polarityFigure])
        else:
            if len(allFigures) - 1 <= 0:
                allFigures.append([polarityFigure])
            else:
                allFigures[len(allFigures) - 1].append(polarityFigure)
        count += 1
        if count > 5: count = 0


    for oneStock, stockTexts in zip(stockList, textPolarities):
        textLen = list(range(1, len(stockTexts) + 1))
        polarityFigure = figure(title=f"{oneStock.name} Article Text Polarity", x_axis_label='Time', y_axis_label='Polarity', height = 300, sizing_mode='scale_width')
        polarityFigure.line(x=textLen, y=stockTexts, legend=oneStock.symbol, line_width=2, color=colors[count])

        if len(allFigures) - 1 > 0 and len(allFigures[len(allFigures) - 1]) >= 2:
            allFigures.append([polarityFigure])
        else:
            if len(allFigures) - 1 <= 0:
                allFigures.append([polarityFigure])
            else:
                allFigures[len(allFigures) - 1].append(polarityFigure)
        count += 1
        if count > 6: count = 0
    

    grid = gridplot(allFigures)

    return components(grid)
    #show(grid)



def biasDashboard(origStock, stockList, compareData):
    '''
    Make a dashboard for the news polarity stuff
    Output it to polarityDashboard.html
    '''
    
    #relevanceBar = barPlot(compareData, "NEWS_SIMILARITY")

    titlePolarities, titleBias, textPolarities, textBias = Analysis.articleSentiments(stockList)

    allFigures = []
    #allFigures.append([relevanceBar])
    #para = Paragraph(text="On this dashboard, you can see the polarity of relevant news articles and headlines. Strongly positive or negative headlines will drive short-term volatility, whereas the polarity of articles impact long-term growth.")

    
    #get averages of each
    means = []
    for oneStockTitles, oneStockTexts in zip(titleBias, textBias):
        if len(oneStockTitles) > 0 and len(oneStockTexts) > 0:
            means.append((statistics.mean(oneStockTitles) + statistics.mean(oneStockTexts)) / 2.0)

    if len(means) > 0:
        xBarNames = compareData["stock_SYMBOL"] #the things that we're listing
        biasBar = figure(x_range=xBarNames, title= "Bias Summary", y_axis_label='Bias', height = 300, sizing_mode='scale_width')
        biasBar.vbar(x=xBarNames, top=means, width=0.9)
    
        allFigures.append([biasBar])
    colors = ["blue", "green", "orange", "purple", "magenta", "cyan", "yellow"]
    count = 1


    for oneStock, stockTitles in zip(stockList, titleBias):
        titleLen = list(range(1, len(stockTitles) + 1))
        polarityFigure = figure(title=f"{oneStock.name} Headline Bias", x_axis_label='Time', y_axis_label='Bias', height = 300, sizing_mode='scale_width')
        polarityFigure.line(x=titleLen, y=stockTitles, legend=oneStock.symbol, line_width=2, color=colors[count])

        if len(allFigures) - 1 > 0 and len(allFigures[len(allFigures) - 1]) >= 2:
            allFigures.append([polarityFigure])
        else:
            if len(allFigures) - 1 <= 0:
                allFigures.append([polarityFigure])
            else:
                allFigures[len(allFigures) - 1].append(polarityFigure)
        count += 1
        if count > 5: count = 0


    for oneStock, stockTexts in zip(stockList, textBias):
        textLen = list(range(1, len(stockTexts) + 1))
        polarityFigure = figure(title=f"{oneStock.name} Article Text Bias", x_axis_label='Time', y_axis_label='Bias', height = 300, sizing_mode='scale_width')
        polarityFigure.line(x=textLen, y=stockTexts, legend=oneStock.symbol, line_width=2, color=colors[count])

        if len(allFigures) - 1 > 0 and len(allFigures[len(allFigures) - 1]) >= 2:
            allFigures.append([polarityFigure])
        else:
            if len(allFigures) - 1 <= 0:
                allFigures.append([polarityFigure])
            else:
                allFigures[len(allFigures) - 1].append(polarityFigure)
        count += 1
        if count > 5: count = 0

    

    grid = gridplot(allFigures)

    return components(grid)



def makeDashboards(symbol, sampleAmount):
    companyList = pd.read_csv("companylist.csv")
    companyRow = companyList[companyList["Symbol"] == symbol]
    retrievedName = companyRow.iat[0, 1]
    retrievedSector = companyRow.iat[0, 7]
    origStock = Scraper.Stock(symbol, retrievedName, retrievedSector)

    #get the comparisons
    compare.experiment(sampleAmount, origStock)
    compareData = pd.read_csv("output.csv")
    compareData = compareData.fillna(0)
    # output to static HTML file

    #get all of the compare stocks
    stockFile = open("stocks.p", "rb")
    stockList = pickle.load(stockFile)

    polarityScript, polarityHtml = polarityDashboard(origStock, stockList, compareData.sort_values(by=['WIKI_SIMILARITY'], ascending = False))
    biasScript, biasHtml = biasDashboard(origStock, stockList, compareData.sort_values(by=['WIKI_SIMILARITY'], ascending = False))
    relScript, relHtml = relevanceDashboard(compareData)
    

    return polarityScript, polarityHtml, biasScript, biasHtml, relScript, relHtml