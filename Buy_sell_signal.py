import investpy as inv
import pandas as pd
import pandas_datareader
from datetime import datetime
import requests
from urllib.request import urlretrieve
import plotly.express as px
import talib as ta
import plotly.graph_objs as go
from stochRSI import computeRSI, stochastic
from supertrend import supertrend

import yfinance as yf

### init table name###
companies = [
    # 'ALE.WA','KGH.WA','PKN.WA', 'LTS.WA', 'PGE.WA', 'DNP.WA',
    "SI=F",
    # 'JSW.WA', "CL=F",
    # 'PZU.WA', 'PKO.WA', "PEO.WA", "CDR.WA", 'CCC.WA', 'CPS.WA', 'LTS.WA', "LPP.WA", "MBK.WA", "PGN.WA", "HG=F",
    ]
dataName = companies[0] + '.csv'
days = "7d"
interval = "1h"

if interval == "1h":
    dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d'
                                                          ' %H:%M:%S'
                                                   )
elif interval == "1d":
    dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d'
                                                   )
data = yf.Ticker(companies[0]).history(period=days, interval=interval)
data = data.set_index(data.index.tz_localize(None))
data.to_csv(f"{dataName}", index=True, encoding="utf-8", index_label="Date")
df = pd.read_csv(f'{dataName}', header=0, index_col='Date', parse_dates=True, date_parser=dateparse).fillna(0)
companies_earn = df
signals = {}
for company in companies:
    dataName = company + '.csv'
    data = yf.Ticker(company).history(period=days, interval=interval)

    data = data.set_index(data.index.tz_localize(None))
    data.to_csv(f"{dataName}", index=True, encoding="utf-8", index_label="Date")
    df = pd.read_csv(f'{dataName}', header=0, index_col='Date', parse_dates=True, date_parser=dateparse).fillna(0)

    #
    trend = supertrend(df,10,5)
    stoploss_Trend = supertrend(df,10,2)
    df = df.join(trend)

    df['RSI'] = computeRSI(df['Close'],10)
    df['k'], df['d'] = stochastic(df['RSI'],7,3,12)

    strong_buy = (f"Strong {company} buy signal")
    weak_buy = (f"Weak {company} buy signal")

    strong_sell = (f"Strong {company} sell signal")
    weak_sell = (f"Weak {company} buy signal")

    # while False != True:
    index = len(df) - 1
    signals[company] = ""
    if df['uptrend'][index] == True:
        if df['k'][index] < 25 or df['d'][index] < 25:
            signals[company] = {f"{strong_buy}"}
        elif df['k'][index] > 25 and df['k'][index] < 75:
            signals[company] = {f"{weak_buy}"}
    elif df['uptrend'][index] == False:
        if df['k'][index] > 75 or df['d'][index] > 75:
            signals[company] = {f"{strong_sell}"}
        elif df['k'][index] > 25 and df['k'][index] < 75:
            signals[company] = {f"{weak_sell}"}


for key in signals:
    print(signals[key])