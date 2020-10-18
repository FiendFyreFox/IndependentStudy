import math

import alpaca_trade_api as tradeapi
import keys
import pandas as pd
import PickStocks
import Analysis
import json
import datetime

import yfinance as yf
from matplotlib import pyplot as plt
'''
api_key = keys.api_key
api_secret = keys.api_secret
base_url = keys.base_url

# instantiate REST API
api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

# obtain account information
account = api.get_account()
print(account)

APCA_API_KEY_ID = api_key
APCA_API_SECRET_KEY = api_secret
APCA_API_BASE_URL = base_url

api = tradeapi.REST(key_id=api_key, secret_key=api_secret, base_url=base_url, api_version='v2')
'''

def invest(amount, confidence, stocks, start=0, end='max'):

    cash_on_hand = amount

    if end == 'max':
        tickers = PickStocks.search(stocks, start)
    else:
        tickers = PickStocks.search(stocks, start, end)

    confidences = []

    for t in tickers:
        confidences.append(Analysis.analyze(t, desiredConfidence=confidence))

    for i in range(0, len(tickers)):
        if confidences[i] > 0:
            buy = confidences[i] / sum(confidences)
            price = yf.Ticker(tickers[i]).history(start=datetime.date.today() - datetime.timedelta(days=1))["Close"][0]
            shares = math.floor((cash_on_hand / price) * buy)
            amount = price * shares
            log(datetime.datetime.now(), tickers[i], shares, amount)
        #buy(c[0], c[1]/sum(confidences))



def log(time, stock, shares, amount, outstanding = True):
    with open("tradebook.json", 'r') as f:
        trades = json.load(f)
    t = str(time)

    if outstanding:
        trades["outstanding"][t] = {}
        trades["outstanding"][t]["stock"] = stock
        trades["outstanding"][t]["shares"] = shares
        trades["outstanding"][t]["amount"] = amount
    else:
        trades["closed"][t] = {}
        trades["closed"][t]["stock"] = stock
        trades["closed"][t]["shares"] = shares
        trades["closed"][t]["amount"] = amount

    with open("tradebook.json", 'w') as f:
        json.dump(trades, f, indent=2)


def clearTradeBook():
    with open("tradebook.json", 'r') as f:
        trades = json.load(f)
    trades["outstanding"] = {}
    trades["closed"] = {}
    with open("tradebook.json", 'w') as f:
        json.dump(trades, f, indent=2)
    print("Successfully cleared the tradebook")

def plot(t, start = datetime.date.today() - datetime.timedelta(days=30), end = datetime.date.today(), interval=1):
    ticker = yf.Ticker(t)
    hist = ticker.history(start=start, end=end, interval=f"{interval}d")
    closes = hist["Close"]
    plt.plot(closes)
    plt.title(t)
    plt.show()

while True:
    i = input("What is your command? >>>")
    if i == "exit":
        exit()
    exec(i)

'''
barset = api.get_barset('AAPL', 'day', limit=5)

aapl_bars = barset['AAPL']
# See how much AAPL moved in that timeframe.
week_open = aapl_bars[0].o
week_close = aapl_bars[-1].c
percent_change = (week_close - week_open) / week_open * 100
print('AAPL moved {}% over the last {} days'.format(percent_change, 5))
'''

