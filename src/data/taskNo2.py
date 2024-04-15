import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
# pip install yfinance
import yfinance as yf
# matplotlib inline


start = "2022-04-15"
end = '2024-04-14'
vertiv = yf.download('VRT',start,end)
cameco = yf.download('CCJ',start,end)
caterpillar = yf.download('CAT',start,end)


vertiv['Volume'].plot(label = 'Vertiv', figsize = (15,7))
cameco['Volume'].plot(label = "Cameco")
caterpillar['Volume'].plot(label = 'Caterpillar Inc.')
plt.title('Volume of Stock traded')
plt.legend()

#Market Capitalisation
vertiv['MarktCap'] = vertiv['Open'] * vertiv['Volume']
cameco['MarktCap'] = cameco['Open'] * cameco['Volume']
caterpillar['MarktCap'] = caterpillar['Open'] * caterpillar['Volume']
vertiv['MarktCap'].plot(label = 'Vertiv', figsize = (15,7))
cameco['MarktCap'].plot(label = 'Cameco')
caterpillar['MarktCap'].plot(label = 'Caterpillar Inc.')
plt.title('Market Cap')
plt.legend()

# Moving Averages for Stock Price Analysis With Python
vertiv['MA50'] = vertiv['Open'].rolling(50).mean()
vertiv['MA200'] = vertiv['Open'].rolling(200).mean()
vertiv['Open'].plot(figsize = (15,7))
vertiv['MA50'].plot()
vertiv['MA200'].plot()

cameco['MA50'] = cameco['Open'].rolling(50).mean()
cameco['MA200'] = cameco['Open'].rolling(200).mean()
cameco['Open'].plot(figsize = (15,7))
cameco['MA50'].plot()
cameco['MA200'].plot()

caterpillar['MA50'] = caterpillar['Open'].rolling(50).mean()
caterpillar['MA200'] = caterpillar['Open'].rolling(200).mean()
caterpillar['Open'].plot(figsize = (15,7))
caterpillar['MA50'].plot()
caterpillar['MA200'].plot()

# Scattered Plot Matrix
data = pd.concat([vertiv['Open'],cameco['Open'],caterpillar['Open']],axis = 1)
data.columns = ['Vertiv[Open]','Cameco[Open]','Caterpillar[Open]']
scatter_matrix(data, figsize = (8,8), hist_kwds= {'bins':250})

# Percentage Increase in Stock Value
#Volatility
vertiv['returns'] = (vertiv['Close']/vertiv['Close'].shift(1)) -1
cameco['returns'] = (cameco['Close']/cameco['Close'].shift(1))-1
caterpillar['returns'] = (caterpillar['Close']/caterpillar['Close'].shift(1)) - 1
vertiv['returns'].hist(bins = 100, label = 'Vertiv', alpha = 0.5, figsize = (15,7))
cameco['returns'].hist(bins = 100, label = 'Cameco', alpha = 0.5)
caterpillar['returns'].hist(bins = 100, label = 'Caterpillar Inc.', alpha = 0.5)
plt.legend()