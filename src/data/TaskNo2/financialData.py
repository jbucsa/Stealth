import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, MonthLocator
from pandas.plotting import scatter_matrix
import seaborn as sns; sns.set()

# Candle Stick Property
def stickColor(close, open):
      if close >= open:
        stickColor = 'green'
      elif close < open:
        stickColor = 'red'
      else: 
        stickColor = 'blue'
      return stickColor

class StockAnalyzer:
  """
  This class facilitates downloading stock data, creating dataframes, 
  and generating plots for specified stocks.
  """
  def __init__(self, start_date, end_date):
    """
    Initializes the StockAnalyzer object with a start and end date for data download.

    Args:
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.
    """
    self.start_date = start_date
    self.end_date = end_date
    self.stocks = {}  # Dictionary to store downloaded stock dataframes

  def add_stock(self, ticker_symbol, stock_name, interval_in_minutes='1mo'):
    """
    interval_in_minutes= 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
    Downloads stock data for the given ticker symbol and stores it in the internal dictionary.

    Args:
        ticker_symbol (str): Ticker symbol of the stock.
    """
    data = yf.download(ticker_symbol, self.start_date, self.end_date, interval=f"{interval_in_minutes}")
    # Earnings
    
    #Market Capitalisation
    data['MarketCap'] = data['Close'] * data['Volume']
    data['Delta'] = data['Open'] - data['Close']
    data['Change'] = data['High'] - data['Low']
    
    self.rev_in_mil = None
    self.rev_in_bil = None
    # Moving Averages for Stock Price Analysis 
    data['MA05'] = data['Open'].rolling(5).mean()
    data['MA10'] = data['Open'].rolling(10).mean()
    data['MA25'] = data['Open'].rolling(25).mean()
    data['MA50'] = data['Open'].rolling(50).mean()
    data['MA100'] = data['Open'].rolling(100).mean()
    data['MA200'] = data['Open'].rolling(200).mean()
    # Candle Sticks
    
    data['candle'] = data[['Open', 'Close']].apply(lambda x: stickColor(open=x[0], close=x[1]), axis=1)
    self.stocks[ticker_symbol] = data
    self.stock_name = stock_name
    
    

  def plot_dataframe_column(self, column_name, figsize=(25, 10), limit_ticks_to_30days=False, ticker_symbol=None, kind="line", x_axis="index"):
    """
    Generates a line plot for the specified column across all downloaded stocks.
    Optionally limits x-axis ticks to 30-day intervals.

    Args:
        column_name (str): Name of the column to plot (e.g., 'Volume', 'Close').
        figsize (tuple, optional): Size of the plot figure. Defaults to (15, 7).
        limit_ticks_to_30days (bool, optional): If True, limits x-axis ticks to 30-day intervals. Defaults to False.
        ticker_symbol (str, optional): Ticker symbol of a specific stock to plot. Defaults to None (plot all stocks).
        kind (str, optional): Type of plot to generate (e.g., 'line', 'scatter'). Defaults to 'line'.
        x_axis (str, optional): Label for the x-axis. Defaults to 'index' (use index as x-axis values).
    """
    if ticker_symbol is None:
      for symbol, data in self.stocks.items():
        data[column_name].plot(label=symbol, figsize=figsize)
        plt.title(f"{column_name} of Stocks")
        plt.legend()

    if ticker_symbol is not None:  # Check if a specific ticker is provided
      data = self.stocks[ticker_symbol]  # Access specific stock data
      data[column_name].plot(label=ticker_symbol, figsize=figsize)
      plt.title(f"{column_name} for {ticker_symbol}")
      plt.legend()
    
    if limit_ticks_to_30days:
      # Set major tick locator to show ticks every 30 days
      plt.gca().xaxis.set_major_locator(MonthLocator(interval=1))
      # Set major tick formatter to format dates as YYYY-MM
      plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m'))

    plt.show()

# Time Range Input
analyzer = StockAnalyzer('2022-04-18', '2024-04-18')
# 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
# Add stocks to analyze

# analyzer.add_stock('BEN', 'Franklin Resources Inc.', interval_in_minutes='60m')

analyzer.add_stock('BEN', 'Franklin Resources Inc.', interval_in_minutes='1d')


# Plot Volume data with limited ticks on x-axis
analyzer.plot_dataframe_column('Volume',  limit_ticks_to_30days=True )

analyzer.plot_dataframe_column('Volume', ticker_symbol='BEN', x_axis='Date')
analyzer.plot_dataframe_column('Close', ticker_symbol='BEN')
analyzer.plot_dataframe_column('MarketCap', ticker_symbol='BEN')
# Plot other data using the same method (e.g., Close, Open, High, Low, Adj Close)


# ... Plot other columns

analyzer.plot_dataframe_column('Volume',  limit_ticks_to_30days=True)
analyzer.stocks['BEN']

# Convert to datetime and extract date
financial_df = analyzer.stocks['BEN']

# Set the date as the new index

earnings_df = pd.read_csv('earnings_df.csv')
earnings_df = earnings_df.set_index('Date')

earnings_df['rev_in_bil'].plot(label='Rev in Billions', figsize=(25,10))
plt.ylim(150, 225) 
plt.title(f"Rev. of BEN in Biilions")
plt.legend()
plt.show()

