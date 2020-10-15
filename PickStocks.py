import pandas as pd
import yfinance as yf
from random import randint
import datetime

allCompanies = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')

#df = allCompanies[0]

#df.to_csv('S&P500-Info.csv')

#randint(0, len(df['Symbol'])

df = pd.read_csv('S&P500-Info.csv')

stock = df['Symbol'][5]

ticker = yf.Ticker(stock)

greatestTicker = ""
greatestIncrease = -999

for i in range(0, 100):


    stock = df['Symbol'][i]
    ticker = yf.Ticker(stock)

    try:
        today = ticker.history(start=datetime.date.today(), interval="1d")["Close"][0]
        lastweek = ticker.history(start=datetime.date.today() - datetime.timedelta(days=5), interval="1d")["Close"][0]
    except:
        continue
    delta = (today / lastweek - 1) * 100

    print(f'The ticker {stock} went up by {delta} %')

    if delta > greatestIncrease:
        greatestTicker = stock
        greatestIncrease = delta

print(f'The greatest increase was {greatestTicker}, which went up by {greatestIncrease} %. On {datetime.date.today() - datetime.timedelta(days=8)} it closed at {yf.Ticker(greatestTicker).history(start=datetime.date.today() - datetime.timedelta(days=8), interval="1d")["Close"][0]}')