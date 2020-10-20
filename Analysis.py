import pandas as pd
import yfinance as yf
import numpy as np
import datetime

#table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')

#df = table[0]

df = pd.read_csv('S&P500-Info.csv')

'''for stock in df["Symbol"][:30]:
    t = yf.Ticker(stock)
    tHist = t.history(start=datetime.date.today() - datetime.timedelta(days=1), period="1d")["Close"]
    today = tHist[1]
    yesterday = tHist[0]

    diff = today / yesterday * 100
    if diff > PMax:
        TMax = stock
        PMax = diff

'''

def analyze(TMax, desiredTrend=15, desiredConfidence = 3.0):
    ticker = yf.Ticker(TMax)
    hist = ticker.history(period="1mo", interval="1d")

    closes = hist["Close"]

    normalizedCloses = []
    for close in closes:
        normalizedCloses.append(close / closes[0] * 1.0)

    average = sum(closes)/len(closes)
    normalizedAverage = average / closes[0]

    deviances = []
    for close in closes:
        deviances.append((close - average) ** 2)

    variance = sum(deviances) / len(deviances)

    stdDev = variance ** (1/2)
    today = closes[len(closes) - 1]
    yesterday = closes[len(closes) - 2]
    yDelta = today - average



    data = normalizedCloses
    x = np.arange(0,len(data))
    y=np.array(data)
    z = np.polyfit(x,y,1)

    confidence = z[0] * 1000 + (2 * yDelta - stdDev) - (stdDev / 2)

    if z[0] * 100 >= desiredTrend / 100 and yDelta > stdDev and confidence > desiredConfidence:
        print(f"I recommend investing in {TMax} stock because it is trending at {z[0] * 100} and recently broke 1 standard deviation by {((yDelta / stdDev) - 1) * 100} %. My confidence in this stock is {confidence}")
        #plt.plot(normalizedCloses)
        #plt.title(TMax)
        #plt.show()
        return confidence
    else:
        print(f"I do not recommend {TMax} stock")
        return 0.0



