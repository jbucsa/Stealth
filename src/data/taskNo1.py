import pandas as pd
import plotly.express as px

df = pd.read_csv(r"../../data/raw/TaskNo1/data.txt", names=['time', 'price'])


if df.empty or df.iloc[-1].isnull().all():
    df = df.iloc[:-1]
    
df.to_csv(r"../../data/interim/TaskNo1/data.cvs", index=False)

with open("../../data/interim/TaskNo1/data.cvs") as f:
    lines = f.readlines()
    last = len(lines) - 1
    lines[last] = lines[last].replace('\r','').replace('\n','')
with open("../../data/interim/TaskNo1/data.cvs", 'w') as wr:
        wr.writelines(lines)

df['time'] = pd.to_datetime(df["time"], unit="ms")


fig = px.line(df, x='time', y='price')
fig.update_xaxes(minor=dict(ticks="inside", showgrid=True))
