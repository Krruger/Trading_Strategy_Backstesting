import investpy as inv
import pandas as pd
import pandas_datareader
from datetime import datetime
import requests
from urllib.request import urlretrieve
import plotly.express as px
import talib as ta
import plotly.graph_objs as go


import yfinance as yf
dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d %H:%M:%S')
company = "JSW.WA"
dataName = company + '.csv'
data = yf.Ticker(company).history(period="100d", interval="1h")

data = data.set_index(data.index.tz_localize(None))
data.to_csv(f"{dataName}", index=True, encoding="utf-8", index_label="Date")
df = pd.read_csv(f'{dataName}', header=0, index_col='Date', parse_dates=True, date_parser=dateparse).fillna(0)
df.head()
rangebreaks = [
        # NOTE: Below values are bound (not single values), ie. hide x to y
        dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
        dict(bounds=[17, 9], pattern="hour"),  # hide hours outside of 9.30am-4pm
        # dict(values=["2020-12-25", "2021-01-01"])  # hide holidays (Christmas and New Year's, etc)
    ]
fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
fig.update_xaxes(
    rangeslider_visible=True,
    rangebreaks=rangebreaks
)
fig.update_layout(
    title='Stock Analysis',
    yaxis_title=f'{company} Stock'
)

fig.show()

# from supertrend import  supertrend
#
# x = supertrend(df)
#
# linear = go.Figure(data=go.Scatter(x=df.index, y=df['upperband']))
# linear.add_trace(go.Scatter(
#     name="Raw Data",
#     mode="lines", x=df.index, y=df["lowerband"]
# ))
# linear.update_xaxes(
#     rangeslider_visible=True,
#     rangebreaks=[
#         # NOTE: Below values are bound (not single values), ie. hide x to y
#         dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
#         dict(bounds=[18, 9], pattern="hour"),  # hide hours outside of 9.30am-4pm
#         # dict(values=["2020-12-25", "2021-01-01"])  # hide holidays (Christmas and New Year's, etc)
#     ]
# )
# linear.update_layout(
#     title='Stock Analysis',
#     yaxis_title=f'{company} Stock'
# )
# linear.show()

from stochRSI import computeRSI, stochastic

df['RSI'] = computeRSI(df['Close'],10)
df['k'], df['d'] = stochastic(df['RSI'],7,3,12)

# from supertrend import  supertrend
#
# x = supertrend(df)

linear = go.Figure(data=go.Scatter(x=df.index, y=df['k']))
linear.add_trace(go.Scatter(
    name="Raw Data",
    mode="lines", x=df.index, y=df["d"]
))

linear.update_xaxes(
    rangeslider_visible=True,
    rangebreaks=[
        # NOTE: Below values are bound (not single values), ie. hide x to y
        dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
        dict(bounds=[18, 9], pattern="hour"),  # hide hours outside of 9.30am-4pm
        # dict(values=["2020-12-25", "2021-01-01"])  # hide holidays (Christmas and New Year's, etc)
    ]
)
linear.update_layout(
    title='Stock Analysis',
    yaxis_title=f'{company} Stock'
)
linear.show()