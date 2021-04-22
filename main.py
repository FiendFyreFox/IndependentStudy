import math
import random

from config import *
import pandas as pd
import PickStocks, Analysis, orders
import json
import datetime

import yfinance as yf
from matplotlib import pyplot as plt
import matplotlib.lines as mlines
import matplotlib.transforms as mtransforms
'''


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

def backtest(stocks, start_date, holding_time, confidence=5, start=0, end='max'):
    buy_date = datetime.datetime(start_date[0], start_date[1], start_date[2])

    if end == 'max':
        tickers = PickStocks.search(stocks, start, date=buy_date)
    else:
        tickers = PickStocks.search(stocks, start, end, date=buy_date)


    confidences = []
    sell_date = buy_date + datetime.timedelta(days=holding_time)

    for t in tickers:
        confidences.append(Analysis.analyze(t, desiredConfidence=confidence, start_date=buy_date, end_date=sell_date))
        #TODO logical issue: analysis is meant to predict AFTER the given period, not during
    #closes = yf.Ticker(tickers[0]).history(start=buy_date, end=sell_date)["Close"][0:5]
    #print(closes)

    purchases = []
    returns = []
    i=0
    for t in tickers:
        if confidences[i] > 0:
            buy_percent = confidences[i] / sum(confidences)
            purchases.append(f"{t}: {buy_percent*100}%")
            closes = yf.Ticker(t).history(start=sell_date, end=sell_date + datetime.timedelta(days=7), interval="1d")["Close"] #TODO add parameter for hold time after purchase
            return_percent = closes[len(closes)-1] / closes[0]
            returns.append(f"{t}: {(return_percent - 1) * 100}%")
        i += 1

    print("I would have invested the following percentages into these stocks:")
    print(purchases)
    print("and earned the following returns:")
    print(returns)

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
            orders.create_order(tickers[i], shares, "buy", type='limit', time_in_force='gtc', limit_price=price * 1.01)

def close_day():

    with open("tradebook.json", 'r') as f:
        trades = json.load(f)

    for trade in trades["outstanding"]:
        orders.create_order(trade["stock"], trade["shares"], side="sell", type="market", time_in_force="gtc")
        trades["closed"][trade] = trade
        trades["closed"][trade]["stock"] = trade["stock"]
        trades["closed"][trade]["shares"] = trade["shares"]
        trades["closed"][trade]["amount"] = trade["amount"]
        del trade

    total = int(orders.get_account()['portfolio_value'])

    print(f'Today a profit of ${total - trades["total_value"]} was made. The total portfolio value now stands at {total}')
    trades["total_value"] = total

    invest(total, 10.0, 30)

    with open("tradebook.json", 'w') as f:
        json.dump(trades, f, indent=2)


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

def closeTrades():
    with open("tradebook.json", 'r') as f:
        trades = json.load(f)
    for trade in trades["outstanding"]:
        #orders.sell(trade["Stock"], trade["Shares"])
        pass

def clearTradeBook():
    with open("tradebook.json", 'r') as f:
        trades = json.load(f)
    trades["outstanding"] = {}
    trades["closed"] = {}
    trades["total_equity"] = {}
    with open("tradebook.json", 'w') as f:
        json.dump(trades, f, indent=2)
    print("Successfully cleared the tradebook")

def analyze(symbol):
    print(Analysis.analyze(symbol))

def plot(t, start = datetime.date.today() - datetime.timedelta(days=30), end = datetime.date.today(), interval=1):
    ticker = yf.Ticker(t)
    hist = ticker.history(start=start, end=end, interval=f"{interval}d")
    closes = hist["Close"]
    plt.plot(closes)
    plt.title(t)
    plt.show()

def order(s, q, side, type, tif='day'):
    print(orders.create_order(s, q, side, type, tif))

def analyze(symbol):
    return Analysis.analyze(symbol)

def o(a, b, c=8):
    tlist = PickStocks.search(10, start=a, end=b)
    for t in tlist:
        Analysis.analyze(t, desiredConfidence=c)

def update_library():
    allCompanies = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')

    df = allCompanies[0]

    df.to_csv('S&P500-Info.csv')

if __name__ == "__main__":
    while True:
        i = input("What is your command? >>> ")
        if i == "exit":
            exit()
        exec(i)



