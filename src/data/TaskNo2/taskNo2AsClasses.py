import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, MonthLocator
from pandas.plotting import scatter_matrix


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

  def add_stock(self, ticker_symbol, stock_name,):
    """
    Downloads stock data for the given ticker symbol and stores it in the internal dictionary.

    Args:
        ticker_symbol (str): Ticker symbol of the stock.
    """
    data = yf.download(ticker_symbol, self.start_date, self.end_date)
    #Market Capitalisation
    data['MarketCap'] = data['Open'] * data['Volume']
    data['Delta'] = data['Open'] - data['Close']
    data['Change'] = data['High'] - data['Low']
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

  def plot_dataframe_column(self, column_name, figsize=(15, 7), limit_ticks_to_30days=False, ticker_symbol=None):
    """
    Generates a line plot for the specified column across all downloaded stocks.
    Optionally limits x-axis ticks to 30-day intervals.

    Args:
        column_name (str): Name of the column to plot (e.g., 'Volume', 'Close').
        figsize (tuple, optional): Size of the plot figure. Defaults to (15, 7).
        limit_ticks_to_30days (bool, optional): If True, limits x-axis ticks to 30-day intervals. Defaults to False.
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

# Example Usage
analyzer = StockAnalyzer('2022-04-15', '2024-04-14')

# Add stocks to analyze
analyzer.add_stock('VRT', 'Vertiv')
analyzer.add_stock('CCJ', 'Cameco')
analyzer.add_stock('CAT', 'Caterpillar Inc.')
analyzer.add_stock('FSLR', 'First Solar')
analyzer.add_stock('BEN', 'Franklin Resources Inc.')
analyzer.add_stock('ET', 'Energy Transfer LP')
analyzer.add_stock('CSCO', 'Cisco Systems Inc.')
analyzer.add_stock('CMCSA', 'Comcast Corp')
analyzer.add_stock('LI', 'Li Auto')
analyzer.add_stock('BWXT', 'BWX Technologies')

# ... Add more stocks as needed

# Plot Volume data with limited ticks on x-axis
analyzer.plot_dataframe_column('Volume',  limit_ticks_to_30days=True)

analyzer.plot_dataframe_column('Volume',  limit_ticks_to_30days=True, ticker_symbol='VRT')

# Plot other data using the same method (e.g., Close, Open, High, Low, Adj Close)
analyzer.plot_dataframe_column('Delta',  limit_ticks_to_30days=True, ticker_symbol='VRT')
# ... Plot other columns

analyzer.plot_dataframe_column('Volume',  limit_ticks_to_30days=True)

analyzer.plot_dataframe_column('Close',  limit_ticks_to_30days=True, ticker_symbol='CAT')

analyzer.plot_dataframe_column('Volume',  limit_ticks_to_30days=True, ticker_symbol='CAT')

analyzer.stocks['CAT']

# Coping a DataFrame from the analyzer function
df_CAT = analyzer.stocks['CAT']['Open']

# Creating a Scatter Plot
data_Scattered = pd.concat([
  analyzer.stocks['VRT']['Open'], 
  analyzer.stocks['CCJ']['Open'], 
  analyzer.stocks['CAT']['Open'], 
  analyzer.stocks['FSLR']['Open'], 
  analyzer.stocks['BEN']['Open'], 
  analyzer.stocks['ET']['Open'],
  analyzer.stocks['CSCO']['Open'], 
  analyzer.stocks['CMCSA']['Open'],  
  analyzer.stocks['LI']['Open'],  
  analyzer.stocks['BWXT']['Open'] ], axis = 1)                                                             
data_Scattered.columns = [ "['VRT']['Open']",
                          "['CCJ']['Open']",
                          "['CAT']['Open']",
                          "['FSLR']['Open']",
                          "['BEN']['Open']",
                          "['ET']['Open']",
                          "['CSCO']['Open']",
                          "['CMCSA']['Open']",
                          "['LI']['Open']",
                          "['BWXT']['Open']"]
scatter_matrix(data_Scattered, figsize = (20,20), hist_kwds= {'bins':250})

analyzer.plot_dataframe_column( 'High',  limit_ticks_to_30days=True, ticker_symbol='VRT')






