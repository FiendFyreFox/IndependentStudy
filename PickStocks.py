import pandas as pd
import yfinance as yf
from random import randint
import datetime

import Analysis

#allCompanies = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')

#df = allCompanies[0]

#df.to_csv('S&P500-Info.csv')

#randint(0, len(df['Symbol'])

df = pd.read_csv('S&P500-Info.csv')

class stock:
    def __init__(self):
        self.delta = -999
        self.ticker = ""

def make_stock():
    s = stock()
    return s


def search(numStocks, start=0, end=len(df["Symbol"]) - 1):
    tickers = []

    for i in range(0, numStocks):
        tickers.append(make_stock())
    print(f'created {len(tickers)} tickers to return')
    for i in range(start, end):


        stock = df['Symbol'][i]
        ticker = yf.Ticker(stock)

        try:
            tHist = ticker.history(start=datetime.date.today() - datetime.timedelta(days=2), period="1d")["Close"]
            today = tHist[1]
            yesterday = tHist[0]
        except:
            continue
        delta = (today / yesterday - 1) * 100

        print(f'The ticker {stock} went up by {delta} %')

        for item in tickers:
            if delta > item.delta:
                item.delta = delta
                item.ticker = stock
                break

    ret = []
    for t in tickers:
        ret.append(t.ticker)

    return ret

#print(f'The greatest increase was {Ticker1}, which went up by {Increase1} %. On {datetime.date.today() - datetime.timedelta(days=1)} it closed at {yf.Ticker(Ticker1).history(start=datetime.date.today() - datetime.timedelta(days=1), interval="1d")["Close"][0]}')

#tHist = yf.Ticker(Ticker1).history(start=datetime.date.today() - datetime.timedelta(days=2), period="1d")["Close"]
#today = tHist[1]
#esterday = tHist[0]
#print(f'{Ticker1} went up from {yesterday} on {datetime.date.today() - datetime.timedelta(days=2)} to {today} on {datetime.date.today() - datetime.timedelta(days=1)}')




#Analysis.plot("BAC", datetime.date.today() - datetime.timedelta(days=30), datetime.date.today())

'''
tHist = yf.Ticker("NFLX").history(start=datetime.date.today() - datetime.timedelta(days=2), period="1d")["Close"]
today = tHist[1]
yesterday = tHist[0]
print(tHist)
print(tHist[0])
print(tHist[1])
'''