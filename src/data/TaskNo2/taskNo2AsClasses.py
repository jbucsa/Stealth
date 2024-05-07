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

# ... Add more stocks as needed

# Plot Volume data with limited ticks on x-axis
analyzer.plot_dataframe_column('Volume',  limit_ticks_to_30days=True )

analyzer.plot_dataframe_column('Volume', ticker_symbol='BEN', x_axis='Date')
analyzer.plot_dataframe_column('Close', ticker_symbol='BEN')
analyzer.plot_dataframe_column('MarketCap', ticker_symbol='BEN')
# Plot other data using the same method (e.g., Close, Open, High, Low, Adj Close)
analyzer.plot_dataframe_column('Delta',  limit_ticks_to_30days=True, ticker_symbol='VRT')
# ... Plot other columns

analyzer.plot_dataframe_column('Volume',  limit_ticks_to_30days=True)

analyzer.plot_dataframe_column('Close',  limit_ticks_to_30days=True, ticker_symbol='CAT')

analyzer.plot_dataframe_column('Volume',  limit_ticks_to_30days=True, ticker_symbol='CAT')

analyzer.stocks['BEN']

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

# Stock that appear related
# VRT & CAT, ET, BWXT 
# CAT & ET
# ET & CAT, BWXT
# BWXT & VRT, CAT, ET

analyzer.plot_dataframe_column( 'Close', ticker_symbol='VRT')
analyzer.plot_dataframe_column( 'Close', ticker_symbol='CAT')
analyzer.plot_dataframe_column( 'Close', ticker_symbol='ET')
analyzer.plot_dataframe_column( 'Close', ticker_symbol='BWXT')

# From here VRT and BWXT appear to have the most in common
analyzer.plot_dataframe_column( 'Close', ticker_symbol='BWXT')
analyzer.plot_dataframe_column( 'Close', ticker_symbol='VRT')

"""
Noted Findings:
  Based on recent news, it appears Vertiv and BWX Technologies are collaborating in the nuclear power industry, specifically involving small modular reactors (SMRs).  BWXT was named the first qualified supplier for GE Vernova's nuclear business' supplier group, which is focused on deploying the BWRX-300 SMR [BWXT Named First Member of GE Vernova Nuclear's Small Modular Reactor Supplier Group]. While the exact nature of their collaboration isn't explicitly stated, it suggests BWX Technologies will likely supply components or materials for the BWRX-300 reactors, and Vertiv's expertise might be relevant in areas like thermal management for these nuclear reactors.

This is just based on recent news, and more information might be available on the companies' websites or through further industry reports.
"""



analyzer.plot_dataframe_column( 'High',  limit_ticks_to_30days=True, ticker_symbol='VRT')


df_CAT  = analyzer.stocks['CAT'].copy()


df_CAT.reset_index(inplace=True)

df_CAT.head()

# plt.figure(figsize=(14,5))
# sns.set_style("ticks")
# sns.lineplot(data=df_CAT, x="Date",y='Close',color='firebrick')
# sns.despine()
# plt.title("The Stock Price of Amazon",size='x-large',color='blue')
