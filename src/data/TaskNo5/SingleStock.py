import pandas as pd
import numpy as np
import itertools
import math

import altair as alt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

import matplotlib.pyplot as plt

from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
import statsmodels.api as sm

import yfinance as yf

Data = yf.download('ET', period='3y', interval='1d', progress=False)

Data

Data['Price_change'] = (Data['Close'][-1] - Data['Close'][0]) / Data['Close'][0]
Data['Ave_vol'] = sum(Data['Volume'])/len(Data['Volume'])
Data['Adj_Score'] = Data['Price_change'] * np.log(Data['Ave_vol'])

Data

df = Data

# Calculating the Slope for the Linear Regression
# Assuming df has a DatetimeIndex, you can extract time indices directly
X = np.arange(len(df)).reshape(-1, 1)  
y = df['Close'].values.reshape(-1, 1)
model = LinearRegression()
model.fit(X, y)
slope = model.coef_[0][0]
print("The estimated slope of the linear regression for the closing price is:", slope)



# Graphing Linear Regression

model = LinearRegression()
model.fit(df.index.values.astype('float64').reshape(-1, 1), df['Close'].values.reshape(-1, 1))  # Use original index values

# Create y_pred values (using original time index)
y_pred = model.predict(df.index.values.astype('float64').reshape(-1, 1))

# Create a DataFrame for plotting, preserving the original DatetimeIndex
df_plot = pd.DataFrame({
    'Time': pd.to_datetime(df.index),  # Convert back to DatetimeIndex
    'Closing Price': df['Close'].values,
    'Predicted Closing Price': y_pred.flatten()
})

# Base chart for both lines and points
base = alt.Chart(df_plot).encode(
    x=alt.X('Time:T', axis=alt.Axis(title='Date')),
    tooltip=['Time', alt.Tooltip('Closing Price:Q', title='Closing Price'), alt.Tooltip('Predicted Closing Price:Q', title='Predicted')]
).properties(
    title='Linear Regression of Closing Price Over Time'
)

# Fit the linear regression model With Scatter Chart
# Create the scatter plot for actual closing prices
scatter_chart_Data_Points = base.mark_circle(size=20).encode(
    y=alt.Y('Closing Price:Q', axis=alt.Axis(title='Price')),
    color=alt.value('steelblue')  # Make points blue
)

# Create the line plot for predicted closing prices
line_chart_Linear_Regression = base.mark_line(color='firebrick').encode(
    y=alt.Y('Predicted Closing Price:Q')
)

# Combine the scatter plot and line plot
combined_chart_Line_With_Scatter = scatter_chart_Data_Points + line_chart_Linear_Regression

# Configure interactive features
combined_chart_Line_With_Scatter = combined_chart_Line_With_Scatter.interactive()  # Allow zooming and panning

# Save the chart
combined_chart_Line_With_Scatter.save('linear_regression_closing_price_over_time.html')  # Save as interactive HTML


# Fit the linear regression model With Line Chart
# Create the Line plot for actual closing prices
line_chart_Data_Points = base.mark_line(color='blue', size=1).encode(
    y=alt.Y('Closing Price:Q', axis=alt.Axis(title='Price')),
    color=alt.value('steelblue')  
)
# Create the line plot for predicted closing prices
line_chart_Linear_Regression = base.mark_line(color='firebrick').encode(
    y=alt.Y('Predicted Closing Price:Q')
)

# Combine the scatter plot and line plot
combined_chart_Line_With_Line = line_chart_Data_Points + line_chart_Linear_Regression

# Configure interactive features
combined_chart_Line_With_Line = combined_chart_Line_With_Line.interactive()  # Allow zooming and panning

# Save the chart
combined_chart_Line_With_Line.save('linear_regression_closing_price_over_time_Line_Vs_Line.html')  # Save as interactive HTML




# ARIMA
# This code does take a long time to run

tickers2021 = ['ET']
Data = {}
for x in tickers2021:
  Data[x] = yf.download(x, period='2y', interval='1d', progress=False)


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
  Scores3.append([x, 100*(forecast[280] - Close[-1])/Close[-1], best_params])

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



revenue = [21.63, 20.53, 20.74, 18.32, 19.00, 20.50, 22.94, 25.95]
gross_profits = [4.77,3.29, 3.34, 2.93, 3.09, 3.17, 2.95, 3.17]
net_income = [1.24, 1.33, 0.584,0.911, 1.11, 1.16 , 1.01 , 1.33] 
adjusted_EBIDTA = [3.62, 3.22, 2.40, 2.72, 2.87, 2.85, 2.70, 3.04]
GAAP_EPS = [0.32, 0.37, 0.31, 0.25, 0.32, 0.34, 0.29, 0.39]
time = ["Q1 '24", "Q4 '23", "Q3 '23", "Q2 '23", "Q1 '23", "Q4 '22", "Q3 '22", "Q2 '22"]


plt.figure(figsize=(12, 6))
plt.subplot(2, 2, 1)
plt.plot(time[::-1], revenue[::-1])
plt.title("Revenue")
plt.ylabel("1B US$")
plt.xticks(rotation=60)
plt.grid()
plt.subplot(2, 2, 2)
plt.plot(time[::-1], net_income[::-1])
plt.title("Net Income")
plt.ylabel("1M US$")
plt.xticks(rotation=60)
plt.grid()
plt.subplot(2, 2, 3)
plt.plot(time[::-1], adjusted_EBIDTA[::-1])
plt.title("Adjusted EBIDTA")
plt.ylabel("1M US$")
plt.xticks(rotation=60)
plt.grid()
plt.subplot(2, 2, 4)
plt.plot(time[::-1], GAAP_EPS[::-1])
plt.title("GAAP Earning per share")
plt.ylabel("US$")
plt.xticks(rotation=60)
plt.grid()

plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.2, hspace=0.4)
plt.show()