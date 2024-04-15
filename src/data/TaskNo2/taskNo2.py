import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
# pip install yfinance
import yfinance as yf
# matplotlib inline

# Date Range
start = '2022-04-15'
end = '2024-04-14'

# Vertiv : VRT
vertiv = yf.download('VRT',start,end)
# Cameco : CCJ
cameco = yf.download('CCJ',start,end)
# Caterpillar Inc. : CAT
caterpillar = yf.download('CAT',start,end)
# First Solar : FSLR
firstSolar = yf.download('FSLR',start,end)
# Franklin Resources Inc. : BEN
frankFranklinResources = yf.download('BEN',start,end)
# Energy Transfer LP : ET
energyTransfer = yf.download('ET',start,end)
# Cisco Systems Inc. : CSCO
cisco = yf.download('CSCO',start,end)
# Comcast Corp : CMCSA
comcast = yf.download('CMCSA',start,end)
# Li Auto : LI
liAuto = yf.download('LI',start,end)
# BWX Technologies : BWXT
bmxTech = yf.download('BWXT',start,end)

vertiv['Volume'].plot(label = 'Vertiv', figsize = (15,7))
cameco['Volume'].plot(label = "Cameco")
caterpillar['Volume'].plot(label = 'Caterpillar Inc.')
firstSolar['Volume'].plot(label = 'First Solar')
frankFranklinResources['Volume'].plot(label = 'Franklin Resources Inc.')
energyTransfer['Volume'].plot(label = 'Energy Transfer LP')
cisco['Volume'].plot(label = 'Cisco Systems Inc.')
comcast['Volume'].plot(label = 'Comcast Corp')
liAuto['Volume'].plot(label = 'Li Auto')
bmxTech['Volume'].plot(label = 'BWX Technologies')
plt.title('Volume of Stock traded')
plt.legend()

vertiv['Close'].plot(label = 'Vertiv', figsize = (15,7))
cameco['Close'].plot(label = "Cameco")
caterpillar['Close'].plot(label = 'Caterpillar Inc.')
firstSolar['Close'].plot(label = 'First Solar')
frankFranklinResources['Close'].plot(label = 'Franklin Resources Inc.')
energyTransfer['Close'].plot(label = 'Energy Transfer LP')
cisco['Close'].plot(label = 'Cisco Systems Inc.')
comcast['Close'].plot(label = 'Comcast Corp')
liAuto['Close'].plot(label = 'Li Auto')
bmxTech['Close'].plot(label = 'BWX Technologies')
plt.title('Closing Price of Stocks')
plt.legend()

vertiv['Open'].plot(label = 'Vertiv', figsize = (15,7))
cameco['Open'].plot(label = "Cameco")
caterpillar['Open'].plot(label = 'Caterpillar Inc.')
firstSolar['Open'].plot(label = 'First Solar')
frankFranklinResources['Open'].plot(label = 'Franklin Resources Inc.')
energyTransfer['Open'].plot(label = 'Energy Transfer LP')
cisco['Open'].plot(label = 'Cisco Systems Inc.')
comcast['Open'].plot(label = 'Comcast Corp')
liAuto['Open'].plot(label = 'Li Auto')
bmxTech['Open'].plot(label = 'BWX Technologies')
plt.title('Opening Price of Stocks')
plt.legend()

vertiv['High'].plot(label = 'Vertiv', figsize = (15,7))
cameco['High'].plot(label = "Cameco")
caterpillar['High'].plot(label = 'Caterpillar Inc.')
firstSolar['High'].plot(label = 'First Solar')
frankFranklinResources['High'].plot(label = 'Franklin Resources Inc.')
energyTransfer['High'].plot(label = 'Energy Transfer LP')
cisco['High'].plot(label = 'Cisco Systems Inc.')
comcast['High'].plot(label = 'Comcast Corp')
liAuto['High'].plot(label = 'Li Auto')
bmxTech['High'].plot(label = 'BWX Technologies')
plt.title('High Price of Stock')
plt.legend()

vertiv['Low'].plot(label = 'Vertiv', figsize = (15,7))
cameco['Low'].plot(label = "Cameco")
caterpillar['Low'].plot(label = 'Caterpillar Inc.')
firstSolar['Low'].plot(label = 'First Solar')
frankFranklinResources['Low'].plot(label = 'Franklin Resources Inc.')
energyTransfer['Low'].plot(label = 'Energy Transfer LP')
cisco['Low'].plot(label = 'Cisco Systems Inc.')
comcast['Low'].plot(label = 'Comcast Corp')
liAuto['Low'].plot(label = 'Li Auto')
bmxTech['Low'].plot(label = 'BWX Technologies')
plt.title('Low Price of Stock')
plt.legend()

vertiv['Adj Close'].plot(label = 'Vertiv', figsize = (15,7))
cameco['Adj Close'].plot(label = "Cameco")
caterpillar['Adj Close'].plot(label = 'Caterpillar Inc.')
firstSolar['Adj Close'].plot(label = 'First Solar')
frankFranklinResources['Adj Close'].plot(label = 'Franklin Resources Inc.')
energyTransfer['Adj Close'].plot(label = 'Energy Transfer LP')
cisco['Adj Close'].plot(label = 'Cisco Systems Inc.')
comcast['Adj Close'].plot(label = 'Comcast Corp')
liAuto['Adj Close'].plot(label = 'Li Auto')
bmxTech['Adj Close'].plot(label = 'BWX Technologies')
plt.title('Adj Close Price of Stock')
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
plt.title('Moving Averages for Vertiv')
plt.legend()


cameco['MA50'] = cameco['Open'].rolling(50).mean()
cameco['MA200'] = cameco['Open'].rolling(200).mean()
cameco['Open'].plot(figsize = (15,7))
cameco['MA50'].plot()
cameco['MA200'].plot()
plt.title('Moving Averages for Cameco')
plt.legend()


caterpillar['MA05'] = caterpillar['Open'].rolling(5).mean()
caterpillar['MA10'] = caterpillar['Open'].rolling(10).mean()
caterpillar['MA20'] = caterpillar['Open'].rolling(20).mean()
caterpillar['MA50'] = caterpillar['Open'].rolling(50).mean()
caterpillar['MA200'] = caterpillar['Open'].rolling(200).mean()
caterpillar['Open'].plot(figsize = (15,7))
caterpillar['MA05'].plot()
caterpillar['MA10'].plot()
caterpillar['MA20'].plot()
caterpillar['MA50'].plot()
caterpillar['MA200'].plot()
plt.title('Moving Averages for Caterpillar Inc.')
plt.legend()

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
plt.title('Percentage Change in Stock Price')
plt.legend()
