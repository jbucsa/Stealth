import pandas as pd
import numpy as np
from datetime import date, timedelta
import yfinance as yf
import matplotlib.pyplot as plt

# Define start and end date (two years back from today)
today = date.today()
two_years_ago = today - timedelta(days=365*2)

# Download Apple stock data
apple_data = yf.download("AAPL", start=two_years_ago, end=today)

# Get closing prices and calculate daily logarithmic returns
closing_prices = apple_data['Close']
daily_returns = np.log(1 + closing_prices.pct_change())

# Estimate mean and standard deviation of daily returns
mean_return = daily_returns.mean()
std_dev = daily_returns.std()

# Define simulation parameters
num_simulations = 1000
num_days = len(closing_prices)

# Simulate future price paths
simulated_prices = np.empty((num_simulations, num_days))
simulated_prices[:, 0] = closing_prices.iloc[-1]  # Start with last closing price

for sim in range(num_simulations):
  for day in range(1, num_days):
    # Simulate daily return using normal distribution
    daily_shock = np.random.normal(mean_return, std_dev)
    simulated_prices[sim, day] = simulated_prices[sim, day-1] * (1 + daily_shock)

# Analyze or visualize the simulated prices (e.g., plot distribution)
plt.hist(simulated_prices[:,-1], bins=50, edgecolor='black')
plt.xlabel('Stock Price')
plt.ylabel('Number of Simulations')
plt.title('Distribution of Simulated Apple Stock Prices (Last Day)')
plt.grid(True)
plt.show()

print("Sample simulated prices at the end:")
print(simulated_prices[:,-1])  # Print last day's price from each simulation


import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import itertools
import statsmodels.api as sm
import math
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

tickers2021 = ['ET']
Data = {}
for x in tickers2021:
  Data[x] = yf.download(x, period='2y', interval='1d', progress=False)


Scores1 = []

for x in tickers2021:
  Price_change = (Data[x]['Close'][-1] - Data[x]['Close'][0]) / Data[x]['Close'][0]
  Ave_vol = sum(Data[x]['Volume'])/len(Data[x]['Volume'])
  Adj_Score = Price_change * math.log(Ave_vol)
  Scores1.append([x, Adj_Score])

Scores1.sort(key=lambda x: x[1], reverse = True)
Top10_1 = Scores1[:10]


slope_parameter = []

for x in tickers2021:
  Temp = Data[x]
  X_train = np.array([i for i in range(len(Temp))]).reshape(-1, 1)
  y_train = Temp['Close'].values.reshape(-1, 1)
  model = LinearRegression()
  model.fit(X_train, y_train)
  slope_parameter.append([x, model.coef_[0][0]])

for x in slope_parameter:
  temp = x[1]*30/Data[x[0]]['Close'][-1]
  x[1] = temp
slope_parameter.sort(key=lambda x: x[1], reverse = True)
Top10_2 = slope_parameter[:10]


Scores3 =[]

for i in range(50):
  x = slope_parameter[i][0]
  Close = Data[x]['Close']
  p = q = range(0, 5)
  d = range(0, 3)
  pdq = list(itertools.product(p, d, q))
  results = []
  for param in pdq:
    try:
        model = sm.tsa.ARIMA(Close, order=param)
        model_fit = model.fit()
        results.append([param, model_fit.aic])
    except:
        continue
  results.sort(key=lambda x: x[1])
  best_params = results[0][0]
  model = sm.tsa.ARIMA(Close, order=best_params)
  model_fit = model.fit()
  forecast = model_fit.forecast(steps= 30)
  Scores3.append([x, 100*(forecast[504] - Close[-1])/Close[-1], best_params])

Scores3.sort(key=lambda x: x[1], reverse = True)

  

Close = Data['ET']['Close']
p = q = range(5, 9)
d = range(3, 5)
pdq = list(itertools.product(p, d, q))
re = []
for param in pdq:
  try:
    model = sm.tsa.ARIMA(Close, order=param)
    model_fit = model.fit()
    re.append([param, model_fit.aic])
  except:
    continue
re.sort(key=lambda x: x[1])
best_params = results[0][0]
model = sm.tsa.ARIMA(Close, order=best_params)
model_fit = model.fit()
forecast = model_fit.forecast(steps= 30)


print(100 * (forecast[504] - Close[-1]) / Close[-1])

print(best_params)

plt.figure(figsize=(10, 6))
plt.plot(Close.index, Close, label='Actual Prices', color='blue')

future_dates = pd.date_range(start=Close.index[-1], periods=31)[1:]
plt.plot(future_dates, forecast, label='Future Predictions', color='red')

plt.title('ARIMA Model Prediction for ET')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()