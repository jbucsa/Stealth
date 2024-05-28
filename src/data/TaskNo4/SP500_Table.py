import pandas as pd
from datetime import datetime

wiki_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

tables = pd.read_html(wiki_url)
sp500_table = tables[0]
sp500_table['Symbol'] #give you all stocks symbols in s&p500

wiki_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

tables = pd.read_html(wiki_url)
sp500_table = tables[0]

# Converts the 'Founded' column into numbers based on the rules need to convert the current object list into a numbers.
def convert_to_number(df, col_name):
  """
  Converts the data type of a column to number with specific rules.

  Args:
      df: The DataFrame containing the column.
      col_name: The name of the column to convert.

  Returns:
      A new DataFrame with the specified column converted to number.
  """
  def g(x):
    try:
      # Check for simple year format
      if pd.isna(x):
        return None
      return int(x)
    except ValueError:
      pass
    try:
      # Extract last four digits if separated by '/'
      return int(x.split('/')[-1])
    except (IndexError, ValueError):
      pass
    try:
      # Extract number within parenthesis
      return int(x.split('(')[-1].split(')')[0])
    except (IndexError, ValueError):
      pass
    return None

  df[col_name] = df[col_name].apply(g)
  return df

# Copies the S&P500 data frame and converts the 'Founded' column into numbers
df = convert_to_number(sp500_table.copy(), 'Founded')


# Filter for stocks founded before the threshold
sp500_filtered = df[df['Founded'] <= 2022]

# Get symbols of the filtered list
sp500_symbols = sp500_filtered['Symbol'].tolist()

# Print the symbols (or use them for further analysis)
print(sp500_symbols)