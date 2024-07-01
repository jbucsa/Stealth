import alpha_vantage.fundamentaldata as av  
# Import fundamentaldata as av
import pandas as pd

from matplotlib.dates import MonthLocator, AutoDateLocator  # Import for date formatting

import datetime
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import matplotlib.dates as dates
import matplotlib.ticker as ticker

# Get your Alpha Vantage API key (replace with yours)
api_key = 'YOUR_API_KEY'

# Create a FundamentalData object with your API key and desired format
fd = av.FundamentalData(key=api_key, output_format='pandas')

# Define the company symbol
symbol = 'ET'

# Get quarterly income statement data
quarterly_earnings, _ = fd.get_income_statement_quarterly(symbol)

# Create a list to store starting fiscal dates
start_dates = []

# Loop through each quarter except the last one to get ending dates
for i in range(len(quarterly_earnings) - 1):
    start_dates.append(quarterly_earnings["fiscalDateEnding"][i+1])

# Add a specific starting date for the last quarter (optional)
start_dates.append("2022-05-27")

# Add a new column "fiscalDateStarting" with converted datetime values
quarterly_earnings["fiscalDateStarting"] = pd.to_datetime(start_dates)

# Filter data for quarters starting from 2022
quarterly_earnings_filtered = quarterly_earnings[quarterly_earnings['fiscalDateStarting'].dt.year >= 2022]

# Extract the first 6 characters (assuming millions) and convert to integers
rev_in_mil = [int(row.totalRevenue[:6]) for row in quarterly_earnings_filtered.itertuples()]

rev_in_bil = [int(row.totalRevenue[0:3]) for row in quarterly_earnings_filtered.itertuples()]

# Add a new column "rev_in_mil" with extracted revenue data
quarterly_earnings_filtered["rev_in_mil"] = rev_in_mil

quarterly_earnings_filtered["rev_in_bil"] = rev_in_bil

quarterly_earnings_filtered.reset_index(inplace=True)
# Remove the "date" column (assuming it's called "date")
quarterly_earnings_filtered = quarterly_earnings_filtered.drop("date", axis=1)

# Set "fiscalDateEnding" as the index
quarterly_earnings_filtered = quarterly_earnings_filtered.set_index("fiscalDateEnding")

# Print the filtered data (optional)
print(quarterly_earnings_filtered)

# Set labels for X and Y axes with custom formatting
fig, main_ax = plt.subplots()
main_ax.plot(quarterly_earnings_filtered['rev_in_bil'])
main_ax.set_ylim(100, np.max(quarterly_earnings_filtered['rev_in_bil']))
main_ax.set_xlabel('Dates')
main_ax.set_ylabel('Rev [$Millions]')
main_ax.set_title('Gaussian colored noise')

plt.show()

earnings_df = quarterly_earnings_filtered.copy()
earnings_df = earnings_df.rename_axis('Date', axis=0)

earnings_df.to_csv('earnings_df.csv', index=True)




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
plt.ylabel("1B US$")
plt.xticks(rotation=60)
plt.grid()
plt.subplot(2, 2, 3)
plt.plot(time[::-1], adjusted_EBIDTA[::-1])
plt.title("Adjusted EBIDTA")
plt.ylabel("1B US$")
plt.xticks(rotation=60)
plt.grid()
plt.subplot(2, 2, 4)
plt.plot(time[::-1], GAAP_EPS[::-1])
plt.title("Earning per share")
plt.ylabel("US$")
plt.xticks(rotation=60)
plt.grid()

plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.2, hspace=0.4)
plt.show()