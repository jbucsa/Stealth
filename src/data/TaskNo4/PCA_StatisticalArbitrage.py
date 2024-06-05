# Import Packages
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats as stats
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA
import scipy
import statsmodels.api as sm
import pandas as pd

from statsmodels.tsa.stattools import coint, grangercausalitytests
import matplotlib

from itertools import groupby, count
import pickle
import yfinance as yf

from dateutil.parser import parse
import datetime

from scipy.optimize import brentq
import traceback

import quantstats as qs
# matplotlib inline

# Allow Multiple Outputs in Cells
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

# Disable Warnings
import warnings
warnings.filterwarnings('ignore')


# Download Stocks
stocks = yf.download('SPY,QQQ', start='2020-1-1', progress=False).Close
stocks.head()

# Equity Curve: PROD(1+R)-1
stocks.pct_change().add(1).cumprod().add(-1).plot()


# Equity Curve of Centered Data i.e. with mean return removed
centered_returns = stocks.pct_change().dropna() - stocks.pct_change().mean()
centered_returns.add(1).cumprod().plot()


# Covariance of Centered Returns
S = centered_returns.cov()
print(S)


# Calculate Eigenvalues and Eigenvectors of Covariance Matrix
E = np.linalg.eig(S)
# EigenValues
print('EigenValues')
eValues=E[0]
eValues
# EigenVectors
print('EigenVectors - Each column is an EigenVector, look closely they are perpendicular!')
eVectors=E[1]
eVectors

# Plot the Correlation of Stock Centered Returns
# 1. Compute Data for Principal Component Lines
x_axis = np.linspace(np.nanmin(centered_returns.SPY), np.nanmax(centered_returns.SPY))
dx1 = eVectors[0,0]
dy1 = eVectors[1,0]
slope1 = dy1/dx1
dx2 = eVectors[0,1]
dy2 = eVectors[1,1]
slope2 = dy2/dx2
y_axis1 = slope1 * x_axis
y_axis2 = slope2 * x_axis
# 2. Plot Centered Return Correlation Between X and Y
plt.plot(centered_returns.SPY, centered_returns.QQQ, '.', alpha=0.25)
# 3. Plot Principal Components
plt.plot(x_axis, y_axis1, label='first component')
plt.plot(x_axis, y_axis2, label='second component')
plt.legend()
plt.xlabel('R0 Values')
plt.ylabel('R1 Values')
plt.show()


# Principal Components and Explained Variance
# Downloading More Instruments
equities = yf.download('GOOG,AMZN,NFLX,BAC,JPM,WFC', start='2020-1-1', progress=False).Close

# Build a PCA Function that returns eigenvectors in order of their sign
def pca(assets):
    x = assets.pct_change().dropna()
    p = np.linalg.eig((x-x.mean()).cov())
    evalues = p[0]
    evectors = p[1]
    # sort
    return np.sort(evalues/sum(evalues))[::-1], evectors[:,np.argsort(evalues)]

# Explained Variance - How many principal components required to explain variance
evalues, evectors = pca(equities)
plt.plot(np.cumsum(evalues), '-o')
plt.title('Number of Principal Components vs Explained Variance')
plt.xlabel('Number of Components')
plt.ylabel('Explained Variance')
plt.show()

# Define our Assets
tech_stocks = yf.download('GOOG,AMZN,NFLX', start='2020-1-1', progress=False).Close
bank_stocks = yf.download('BAC,JPM,WFC', start='2020-1-1', progress=False).Close
commodities = yf.download('CL=F,RB=F,GC=F', start='2020-1-1', progress=False).Close


# Factor Analysis
r = []
lookback = 50

r.append(tech_stocks['GOOG'].pct_change().iloc[-lookback:].values)
r.append(tech_stocks['AMZN'].pct_change().iloc[-lookback:].values)
r.append(tech_stocks['NFLX'].pct_change().iloc[-lookback:].values)

r.append(bank_stocks['BAC'].pct_change().iloc[-lookback:].values)
r.append(bank_stocks['JPM'].pct_change().iloc[-lookback:].values)
r.append(bank_stocks['WFC'].pct_change().iloc[-lookback:].values)

r.append(commodities['CL=F'].pct_change().iloc[-lookback:].values) # Cr
r.append(commodities['RB=F'].pct_change().iloc[-lookback:].values) # RB
r.append(commodities['GC=F'].pct_change().iloc[-lookback:].values) # Go

R = np.array(r)

# Eigen System: Element [0]=eValues, [1]=eVectors
eigenSystem = np.linalg.eig(np.cov(R-np.mean(R)))

# Plot Results by Eigen Value Components
colour = ['r']*3 + ['b']*3 + ['g']*3

# Plot Assets
for j,i in enumerate(eigenSystem[1]):
    plt.plot(i[0], i[1], '-o', c=colour[j], ms=10)

# Plot Circle
for i in np.linspace(-np.pi, np.pi, 1500):
    plt.plot(np.cos(i), np.sin(i), 'k.', ms=0.3)
    
plt.title('Factor Groupings')
plt.xlabel('first component')
plt.ylabel('second component')
plt.axis('equal')
plt.show();

# Factor Analysis Automation