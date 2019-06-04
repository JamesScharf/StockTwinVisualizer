import numpy as np # we will use this later, so import it now
import pandas as pd
from bokeh.io import output_notebook, show
from bokeh.plotting import figure
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure


def do_sums(df):
    cat = df["stock_SYMBOL"].tolist()#['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
    freq = df["WIKI_SIMILARITY"].tolist()

    source = ColumnDataSource(data=dict(cat=cat, freq=freq, color=Spectral6))

    p = figure(x_range=cat, y_range=(0,1), plot_height=250, title="WIKI_SIMILARITY",
               toolbar_location=None, tools="")

    p.vbar(x='cat', top='freq', width=0.9, color='color', legend="cat", source=source)

    p.xgrid.grid_line_color = None
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"

    show(p)

def do_news(df):
    cat = df["stock_SYMBOL"].tolist()#['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
    freq = df["NEWS_SIMILARITY"].tolist()
    #LINK_SIMILARITY,REFERENCE SIMILARITY

    source = ColumnDataSource(data=dict(cat=cat, freq=freq, color=Spectral6))

    p = figure(x_range=cat, y_range=(0,1), plot_height=250, title="NEWS_SIMILARITY",
               toolbar_location=None, tools="")

    p.vbar(x='cat', top='freq', width=0.9, color='color', legend="cat", source=source)

    p.xgrid.grid_line_color = None
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"

    show(p)

def do_lin(df):
    cat = df["stock_SYMBOL"].tolist()#['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
    freq = df["LINK_SIMILARITY"].tolist()
    #,REFERENCE SIMILARITY

    source = ColumnDataSource(data=dict(cat=cat, freq=freq, color=Spectral6))

    p = figure(x_range=cat, y_range=(0,1), plot_height=250, title="LINK_SIMILARITY",
               toolbar_location=None, tools="")

    p.vbar(x='cat', top='freq', width=0.9, color='color', legend="cat", source=source)

    p.xgrid.grid_line_color = None
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"

    show(p)

def do_ref(df):
    cat = df["stock_SYMBOL"].tolist()#['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
    freq = df["REFERENCE SIMILARITY"].tolist()
    #,

    source = ColumnDataSource(data=dict(cat=cat, freq=freq, color=Spectral6))

    p = figure(x_range=cat, y_range=(0,1), plot_height=250, title="REFERENCE SIMILARITY",
               toolbar_location=None, tools="")

    p.vbar(x='cat', top='freq', width=0.9, color='color', legend="cat", source=source)

    p.xgrid.grid_line_color = None
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"

    show(p)






if __name__ == '__main__':
    df = pd.read_csv("output.csv")
    output_file("graphs.html")

    do_sums(df)
    do_news(df)
    do_ref(df)
    do_lin(df)
