import pandas as pd
import numpy as np
import itertools
import math

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

