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

import yfinance as yf
import pandas as pd
from pmdarima.arima import auto_arima
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

def download_and_arima(ticker, start_date, end_date):
    # Download data
    data = yf.download(ticker, start=start_date, end=end_date)["Adj Close"]

    # Automatic ARIMA model selection
    auto_model = auto_arima(
        data, 
        start_p=5, max_p=9, 
        start_q=5, max_q=9,
        start_d=3, max_d=5,
        seasonal=False,
        trace=True
    )
    
    # Fit the best ARIMA model
    model = ARIMA(data, order=auto_model.order)
    model_fit = model.fit()

    # Make predictions
    forecast = model_fit.get_forecast(steps=30)  # Predict next 30 days
    forecasted_values = forecast.predicted_mean
    confidence_intervals = forecast.conf_int()

    # Plot results
    plt.figure(figsize=(12, 6))
    plt.plot(data, label="Actual Prices")
    plt.plot(forecasted_values, label="Forecasted Prices", color="red")
    plt.fill_between(
        confidence_intervals.index,
        confidence_intervals.iloc[:, 0],
        confidence_intervals.iloc[:, 1],
        color="gray",
        alpha=0.2
    )
    plt.xlabel("Date")
    plt.ylabel("Adjusted Closing Price")
    plt.title(f"ARIMA Model for {ticker}")
    plt.legend()
    plt.show()

# Get user input
ticker = input("Enter stock ticker symbol (e.g., AAPL): ")
start_date = input("Enter start date (YYYY-MM-DD): ")
end_date = input("Enter end date (YYYY-MM-DD): ")

# Run the analysis
download_and_arima(ticker='ET', start_date='2022-01-01', end_date='2024-05-27')