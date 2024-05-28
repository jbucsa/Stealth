import yfinance as yf
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt

# Define stock ticker symbol and prediction period
ticker = "AAPL"  # Replace with your desired stock ticker
periods = 3

# Download historical data
data = yf.download(ticker, period="max")

# Check for empty data
if len(data) == 0:
  print("Error: No data downloaded for", ticker)
  exit()

# Ensure datetime index
if not pd.api.types.is_datetime64_dtype(data.index):
  # Convert index to datetime if necessary
  data.index = pd.to_datetime(data.index)

# Define endogenous (variable to predict)
endog = data["Close"].copy()

# Select closing price
data = data["Close"]



# Define filter for dates (last 2 years + next 6 months)
two_years_ago = data.index[-1] + pd.DateOffset(years=-2)
future_end_date = data.index[-1] + pd.DateOffset(months=periods)

# Filter data for plotting
filtered_data = data[(data.index >= two_years_ago), (data.index <= future_end_date)]

# Fit SARIMAX model (adjust parameters as needed)
model = SARIMAX(filtered_data, trend=[0,0,2,0], order=(1, 1, 2), seasonal_order=(1, 1, 1, 12))
model_fit = model.fit()

# Generate forecast
forecast = model_fit.forecast(periods)

# Prepare data for plotting (using list conversion)
dates_list = filtered_data.index.tolist()  # Convert Timestamps to list (order might be lost)
future_dates_list = [filtered_data.index[-1] + pd.DateOffset(months=x) for x in range(1, periods + 1)]

# Plot actual and predicted values
plt.figure(figsize=(10, 6))
plt.plot(dates_list, filtered_data, label="Actual Price")
plt.plot(future_dates_list, forecast, label="Predicted Price")
plt.xlabel("Index")  # Update label to reflect list usage
plt.ylabel("Closing Price")
plt.title(f"SARIMAX Forecast for {ticker} - Next {periods} Months")
plt.legend()
plt.grid(True)

# Limit x-axis range for desired timeframe
plt.xlim(two_years_ago, future_end_date)

plt.show()

print(f"Forecast for the next {periods} months:")
print(forecast)




