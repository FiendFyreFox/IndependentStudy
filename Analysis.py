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

def analyze(TMax, desiredTrend=15, desiredConfidence = 3.0, start_date=None, end_date=None):
    ticker = yf.Ticker(TMax)

    if start_date == None:
        hist = ticker.history(period="1mo", interval="1d")
    else:
        hist = ticker.history(start=start_date, end=end_date, interval="1d")

    closes = hist["Close"]

    normalizedCloses = []
    for close in closes:
        normalizedCloses.append(close / closes[0] * 1.0)
    try:
        average = sum(closes)/len(closes)
    except:
        return 0.0
    normalizedAverage = average / closes[0]

    deviances = []
    for close in normalizedCloses:
        deviances.append((close - normalizedAverage) ** 2)

    variance = sum(deviances) / len(deviances)

    stdDev = variance ** (1/2)
    today = closes[len(closes) - 1]
    yesterday = closes[len(closes) - 2]
    yDelta = today/closes[0] - normalizedAverage



    data = normalizedCloses
    x = np.arange(0,len(data))
    y=np.array(data)
    z = np.polyfit(x,y,1)

    confidence = z[0] * 2000 + (yDelta / stdDev) - (stdDev)

    if z[0] * 100 >= desiredTrend / 100 and yDelta > stdDev and confidence > desiredConfidence: #TODO Solve this gibberish
        print(f"I recommend investing in {TMax} stock because it is trending at {z[0] * 100} and recently broke 1 standard deviation by {((yDelta / stdDev) - 1) * 100} %. My confidence in this stock is {confidence}")
        #plt.plot(normalizedCloses)
        #plt.title(TMax)
        #plt.show()
        return confidence
    elif confidence > desiredConfidence:
        print(f"I somewhat recommend investing in {TMax} stock, however it fails to meet certain thresholds.")
        return confidence - 1
    else:
        print(f"I do not recommend {TMax} stock (confidence: {confidence})")
        return 0.0



