import pandas as pd
import plotly.express as px

# Creates a DataFrame from a TXT 'data.txt' file
df = pd.read_csv("../../data/raw/TaskNo1/data.txt", delimiter=",", header=None)

# Removes any blanks ROW from the NEW DataFrame
if df.empty or df.iloc[-1].isnull().all():
    df = df.iloc[:-1]

# Adds LABELS the Columns of the DataFrame. 
# DOES NOT ADD A LABEL TO THE INDEX COLUMN 
df.columns = ["time", "price"]

# Converts the time column from Linux time to typical date schema in the DataFrame 
df['time'] = pd.to_datetime(df["time"], unit="ms")

# Saves the DataFrame to a NEW .CSV file
df.to_csv("../../data/interim/TaskNo1/data.csv", index=False)

# Removes any blanks ROW that may have been created in the NEW .CSV file.
with open("../../data/interim/TaskNo1/data.csv") as f:
    lines = f.readlines()
    last = len(lines) - 1
    lines[last] = lines[last].replace('\r','').replace('\n','')
with open("../../data/interim/TaskNo1/data.csv", 'w') as wr:
        wr.writelines(lines)


# Plotting a LINE-GRAPH were we set the COLUMN='time' to X-AXIS and COLUMN='price' to Y-AXIS
fig = px.line(df, x='time', y='price')
fig.update_xaxes(minor=dict(ticks="inside", showgrid=True))
