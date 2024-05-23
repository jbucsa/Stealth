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
