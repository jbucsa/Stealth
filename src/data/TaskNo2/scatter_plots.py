import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, MonthLocator
from pandas.plotting import scatter_matrix
import seaborn as sns; sns.set()
import numpy as np


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
analyzer = StockAnalyzer('2022-05-10', '2024-05-10')
# 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
# Add stocks to analyze
analyzer.add_stock('VRT', 'Vertiv', interval_in_minutes='1d')
analyzer.add_stock('CCJ', 'Cameco', interval_in_minutes='1d')
analyzer.add_stock('CAT', 'Caterpillar Inc.', interval_in_minutes='1d')
analyzer.add_stock('FSLR', 'First Solar', interval_in_minutes='1d')
analyzer.add_stock('BEN', 'Franklin Resources Inc.', interval_in_minutes='1d')
analyzer.add_stock('ET', 'Energy Transfer LP', interval_in_minutes='1d')
analyzer.add_stock('CSCO', 'Cisco Systems Inc.', interval_in_minutes='1d')
analyzer.add_stock('CMCSA', 'Comcast Corp', interval_in_minutes='1d')
analyzer.add_stock('LI', 'Li Auto', interval_in_minutes='1d')
analyzer.add_stock('BWXT', 'BWX Technologies', interval_in_minutes='1d')

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


np.corrcoef( analyzer.stocks['VRT']['Close'], 
  analyzer.stocks['CAT']['Close'])
np.corrcoef( analyzer.stocks['VRT']['Close'], 
  analyzer.stocks['ET']['Close'] )
np.corrcoef( analyzer.stocks['VRT']['Close'],   
  analyzer.stocks['BWXT']['Close'] )
np.corrcoef( analyzer.stocks['CAT']['Close'], 
  analyzer.stocks['ET']['Close'])
np.corrcoef(analyzer.stocks['CSCO']['Close'],  
  analyzer.stocks['BEN']['Close'] )



class StockScatterAnalyzer:
  """
  This class facilitates generating scatter plots and calculating correlation coefficients 
  for stock data from a StockAnalyzer object.
  """

  def __init__(self, analyzer):
    """
    Initializes the StockScatterAnalyzer with a StockAnalyzer object.

    Args:
        analyzer (StockAnalyzer): The StockAnalyzer object containing downloaded stock data.
    """
    self.analyzer = analyzer
    self.default_column = 'Close'  # Default column to show on the scatter plot
    
  def plot_scatter_correlation(self, selected_stocks=None , column=None):
    """
    Generates a scatter matrix with correlation coefficients for selected stocks.

    Args:
        selected_stocks (list, optional):
          List of ticker symbols for specific stocks to plot. 
          Defaults to all stocks in the StockAnalyzer object.
        column (str, optional): 
          The specific column to use for the scatter plot. 
          Defaults to the default_column ('Close').
    """
    # Select data for plotting based on selected stocks
    if selected_stocks is None:
      data_to_plot = self.analyzer.stocks
    else:
      data_to_plot = {symbol: data for symbol, data in self.analyzer.stocks.items() if symbol in selected_stocks}

    # Extract data as DataFrame, considering user-specified column
    column_to_use = column if column is not None else self.default_column
    data_list = [data[column_to_use] for symbol, data in data_to_plot.items()]
    data_Scattered = pd.concat(data_list, axis=1, keys=data_to_plot.keys())

    # Create figure and subplots with desired layout
    fig, axes = plt.subplots(len(data_Scattered.columns), len(data_Scattered.columns), figsize=(20, 20))
    
    # Create scatter matrix
    matrix = scatter_matrix(data_Scattered, figsize=(20, 20), alpha=0.8, diagonal='hist', hist_kwds={'bins': 250})

    # Calculate correlation matrix
    correlation_matrix = np.corrcoef(data_Scattered.values.T)

     # Loop through subplots and add correlation coefficient as annotation
    for i in range(len(data_Scattered.columns)):
        for j in range(len(data_Scattered.columns)):
            if i > j:  # Skip diagonal plots
                ax = axes[i, j]  # Access subplot axes
                corr_value = correlation_matrix[i, j]
                ax.annotate(f"{corr_value:.2f}", xy=(0.8, 0.8), xycoords='axes fraction', ha='center', va='center')

    plt.suptitle(f'Scatter Matrix with Correlation Coefficients for {column} values',fontsize=12)
    plt.show()


scatter_analyzer = StockScatterAnalyzer(analyzer)


# Plot scatter matrix for all stocks (default 'Close' column)
scatter_analyzer.plot_scatter_correlation()

# Plot scatter matrix for specific stocks with a different column ('Open')
selected_stocks = ['VRT', 'CAT', 'ET']
scatter_analyzer.plot_scatter_correlation(selected_stocks, column='Open')










