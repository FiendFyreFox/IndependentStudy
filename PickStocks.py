import pandas as pd
import yfinance as yf
import datetime
import time

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


def search(numStocks, start=0, end=len(df["Symbol"]) - 1, date=(datetime.date.today() - datetime.timedelta(days=5))):
    tickers = []

    for i in range(0, numStocks):
        tickers.append(make_stock())
    print(f'created {len(tickers)} tickers to return')
    for i in range(start, end):


        stock = df['Symbol'][i]
        ticker = yf.Ticker(stock)

        try:
            tHist = ticker.history(start=date, period="1d")["Close"]
            today = tHist[len(tHist) - 1]
            yesterday = tHist[len(tHist) - 2]
        except:
            continue
        delta = (today / yesterday - 1) * 100

        progressBar(i - start, end - start)

        for item in tickers:
            if delta > item.delta:
                item.delta = delta
                item.ticker = stock
                break

    print ('\n') # this is here to make sure that the first stock doesn't print on top of the progress bar TODO make it work
    ret = []
    for t in tickers:
        ret.append(t.ticker)

    return ret

def progressBar(current, total, barLength = 20):
    percent = float(current) * 100 / total
    arrow   = '-' * int(percent/100 * barLength - 1) + '>'
    spaces  = ' ' * (barLength - len(arrow))
    hmm ='Progress: [%s%s] %d %%' % (arrow, spaces, percent)
    #print(hmm, end='\x1b[2K\r')
    print("\r", hmm, end="") #TODO make sure this is in desktop code

if __name__ == '__main__':
    progressBar(50, 100)
    for i in range (0, 3):
        print('abc'[i], end='\r')
        time.sleep(1)