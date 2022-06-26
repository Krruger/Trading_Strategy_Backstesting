import investpy as inv
import pandas as pd
import pandas_datareader
from datetime import datetime
import requests
from urllib.request import urlretrieve
import plotly.express as px
import talib as ta
import plotly.graph_objs as go
from pandas_ta import adx, dm, sma
import numpy as np
import yfinance as yf

### init table name###
companies = [
    'ALE.WA',
    'KGH.WA',
    'PKN.WA',
    'LTS.WA',
    'PGE.WA',
    'DNP.WA', 'CPS.WA'
             'JSW.WA',
             'PZU.WA', 'PKO.WA', "PEO.WA",
             "CDR.WA", 'MBK.WA'
# "SI=F",
             ]
dataName = companies[0] + '.csv'
days = "365d"
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
companies_earn["zysk"] = 0
for company in companies:
    dataName = company + '.csv'
    data = yf.Ticker(company).history(period=days, interval=interval)

    data = data.set_index(data.index.tz_localize(None))
    data.to_csv(f"{dataName}", index=True, encoding="utf-8", index_label="Date")
    df = pd.read_csv(f'{dataName}', header=0, index_col='Date', parse_dates=True, date_parser=dateparse).fillna(0)
    # df.head()
    # rangebreaks = [
    #         # NOTE: Below values are bound (not single values), ie. hide x to y
    #         dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
    #         dict(bounds=[17, 9], pattern="hour"),  # hide hours outside of 9.30am-4pm
    #         # dict(values=["2020-12-25", "2021-01-01"])  # hide holidays (Christmas and New Year's, etc)
    #     ]
    # fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
    # fig.update_xaxes(
    #     rangeslider_visible=True,
    #     rangebreaks=rangebreaks
    # )
    # fig.update_layout(
    #     title='Stock Analysis',
    #     yaxis_title=f'{company} Stock'
    # )
    #
    # fig.show()

    from supertrend import  supertrend
    #
    trend = supertrend(df,12,6)
    stoploss_Trend = supertrend(df,10,2)
    df = df.join(trend)
    ADX = adx(df['High'], df['Low'], df['Close'])
    df = df.join(ADX)
    SMA = sma(df['Close'], 200)
    df = df.join(SMA)
    #
    # linear = go.Figure(data=go.Scatter(x=df.index, y=x['supertrend']))
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


    # x = supertrend(df)

    # linear = go.Figure(data=go.Scatter(x=df.index, y=df['k'], name="k"))
    # linear.add_trace(go.Scatter(
    #     name="d",
    #     mode="lines", x=df.index, y=df["d"]
    # ))
    #
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
    # import pandas_ta as ta
    # df['stoploss'] = ta.supertrend(df['High'], df['Low'], df['Close'], 10, 3)

    ## =================== Strategy ===================== ##
    # x = pd.DataFrame([], df.index)
    # x['supertrend'] = None
    # for index in range(len(df)):
    #     if df['in_uptrend'][index] == True:
    #         x['supertrend'][index] = df['lowerband'][index]
    #     else:
    #         x['supertrend'][index] = df['upperband'][index]
    #
    # def zoom(layout, xrange):
    #     in_view = df.loc[fig.layout.xaxis.range[0]:fig.layout.xaxis.range[1]]
    #     fig.layout.yaxis.range = [in_view.High.min() - 10, in_view.High.max() + 10]
    #
    # fig.layout.on_change(zoom, 'xaxis.range')
    #
    # rangebreaks = [
    #         # NOTE: Below values are bound (not single values), ie. hide x to y
    #         dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
    #         dict(bounds=[18, 9], pattern="hour"),  # hide hours outside of 9.30am-4pm
    #         # dict(values=["2020-12-25", "2021-01-01"])  # hide holidays (Christmas and New Year's, etc)
    #     ]
    # fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
    # fig.add_trace(go.Scatter(
    #     name="d",
    #     mode="lines", x=df.index, y=x['supertrend']
    # ))
    # fig.update_xaxes(
    #     rangeslider_visible=False,
    #     rangebreaks=rangebreaks
    # )
    # fig.update_layout(
    #     title='Stock Analysis',
    #     yaxis_title=f'{company} Stock'
    # )
    #
    # fig.show()

    k_d_different = 4
    df['long'] = None
    df[f"{company}"] = None
    position = None
    kapitał = 2000
    zysk = 0
    lewar = 1
    take_profit = 0.05
    stoploss_margin_call = take_profit
    adx_value = 30
    ret = 0
    tranzakcje_zyskowne = 0
    tranzakcje_stratne = 0
    total_return = {}
    for current in range(len(df)):
        previous = current - 1
        #In uptrend
        if df['uptrend'][current] == True and position == None:
                # and position == None and df["Close"][current] > df['SMA_200'][current]:
            if df['k'][current] < 40 and df['k'][current] - df['d'][current] >= k_d_different and df['ADX_14'][current] > adx_value:
                df['long'][current] = True
                position = df['long'][current]
                akcje = kapitał/df['Close'][current]
                long_start_data = data.index[current]
                position_price = df['Close'][current]
                print(f"{company} Otwarto pozycje long dnia {df.index[current]} po cenie {df['Close'][current]}")


        #In lowertrend
        if df['uptrend'][current] == False and position == None:
                # and position == None and df["Close"][current] < df['SMA_200'][current]:
            if df['k'][current] > 60 and df['k'][current] - df['d'][current] <= -k_d_different and df['ADX_14'][current] > adx_value:
                df['long'][current] = False
                position = df['long'][current]
                akcje = kapitał / df['Close'][current]
                short_start_data = data.index[current]
                position_price = df['Close'][current]
                print(f"{company} Otwarto pozycje short dnia {df.index[current]} po cenie {df['Close'][current]}")

        # #sell long
        # if position == True:
        #     if df['k'][current] > 75 and df['k'][current] <= df['d'][current]:
        #         position = None
        #         after_sell = (akcje * df['Close'][current])
        #         zysk_z_transakcji = (after_sell - kapitał) * lewar
        #         zysk = zysk + zysk_z_transakcji
        #         print(f"Pozycja long otwarta dnia {long_start_data} została zamknięta dnia {df.index[current]} po cenie {df['Close'][current]}."
        #         f"\n Zysk z transakcji {zysk_z_transakcji} ")

        # #sell short
        # if position == False:
        #     if df['k'][current] < 25 and df['k'][current] >= df['d'][current]:
        #         position = None
        #         after_sell =  (akcje * df['Close'][current])
        #         if after_sell > 1000:
        #             zysk_z_transakcji = (after_sell - kapitał) * lewar
        #             zysk = zysk - zysk_z_transakcji
        #         else:
        #             zysk_z_transakcji = abs(after_sell - kapitał) * lewar
        #             zysk = zysk + zysk_z_transakcji
        #         print(f"Pozycja short otwarta dnia {short_start_data} została zamknięta dnia {df.index[current]} po cenie {df['Close'][current]}."
        #         f"\n Zysk z transakcji {zysk_z_transakcji}")

        #takeprofit long
        if position == True:
            if df['Close'][current] > (position_price * (1+take_profit)):
                position = None
                after_sell = (akcje * df['Close'][current])
                zysk_z_transakcji = (after_sell - kapitał) * lewar
                zysk = zysk + zysk_z_transakcji
                print(f"{company} Pozycja long otwarta dnia {long_start_data} została zamknięta dnia {df.index[current]} po cenie {df['Close'][current]}."
                f"\n Zysk z transakcji {zysk_z_transakcji}")
                tranzakcje_zyskowne += 1
        #takeprofit short
        if position == False:
            if df['Close'][current] < (position_price * (1-take_profit)):
                position = None
                after_sell =  (akcje * df['Close'][current])
                if after_sell > kapitał:
                    zysk_z_transakcji = (after_sell - kapitał) * lewar
                    zysk = zysk - zysk_z_transakcji
                else:
                    zysk_z_transakcji = abs(after_sell - kapitał) * lewar
                    zysk = zysk + zysk_z_transakcji
                print(f"{company} Pozycja short otwarta dnia {short_start_data} została zamknięta dnia {df.index[current]} po cenie {df['Close'][current]}."
                f"\n Zysk z transakcji {zysk_z_transakcji}")
                tranzakcje_zyskowne += 1

        # Long stoploss
        if position == True and df['Close'][current] < position_price * (1- stoploss_margin_call) :
            position = None
            after_sell = (akcje * df['Close'][current])
            if after_sell > kapitał:
                zysk_z_transakcji = (after_sell - kapitał) * lewar
                zysk = zysk + zysk_z_transakcji
                print(f"{company} STOPLOSS Pozycja long otwarta dnia {long_start_data} została zamknięta dnia {df.index[current]} po cenie {df['Close'][current]}."
                      f"\n Zysk z transakcji {zysk_z_transakcji}")
            else:
                strata_z_transakcji = (after_sell - kapitał) * lewar
                zysk = zysk + strata_z_transakcji
                print(f"{company} STOPLOSS Pozycja long otwarta dnia {long_start_data} została zamknięta dnia {df.index[current]} po cenie {df['Close'][current]}."
                      f"\n Strata z transakcji {strata_z_transakcji}")
            tranzakcje_stratne += 1
        #Short stoploss
        if position == False and df['Close'][current] > position_price * (1 + stoploss_margin_call):
            position = None
            after_sell = (akcje * df['Close'][current])
            if after_sell > kapitał:
                strata_z_transakcji = (after_sell - kapitał) * lewar
                zysk = zysk - strata_z_transakcji
                print(f"{company} STOPLOSS Pozycja short otwarta dnia {short_start_data} została zamknięta dnia {df.index[current]} po cenie {df['Close'][current]}."
                      f"\n Strata z transakcji {-strata_z_transakcji}")
            else:
                zysk_z_transakcji = abs(after_sell - kapitał) * lewar
                zysk = zysk + zysk_z_transakcji
                print(f"{company} STOPLOSS Pozycja short otwarta dnia {short_start_data} została zamknięta dnia {df.index[current]} po cenie {df['Close'][current]}."
                      f"\n Zysk z transakcji {zysk_z_transakcji}")
            tranzakcje_stratne += 1

        # #Long stoploss
        # if position == True and stoploss_Trend['uptrend'][current] == False:
        #     position = None
        #     after_sell = (akcje * df['Close'][current])
        #     if after_sell > 1000:
        #         zysk_z_transakcji = (after_sell - kapitał) * lewar
        #         zysk = zysk + zysk_z_transakcji
        #         print(f"STOPLOSS Pozycja long otwarta dnia {long_start_data} została zamknięta dnia {df.index[current]}."
        #               f"\n Zysk z transakcji {zysk_z_transakcji}")
        #     else:
        #         strata_z_transakcji = (after_sell - kapitał) * lewar
        #         zysk = zysk + strata_z_transakcji
        #         print(f"STOPLOSS Pozycja long otwarta dnia {long_start_data} została zamknięta dnia {df.index[current]}."
        #               f"\n Strata z transakcji {strata_z_transakcji}")
        # #Short stoploss
        # if position == False and stoploss_Trend['uptrend'][current] == True:
        #     position = None
        #     after_sell = (akcje * df['Close'][current])
        #     if after_sell > 1000:
        #         strata_z_transakcji = (after_sell - kapitał) * lewar
        #         zysk = zysk - strata_z_transakcji
        #         print(f"STOPLOSS Pozycja short otwarta dnia {short_start_data} została zamknięta dnia {df.index[current]}."
        #               f"\n Strata z transakcji {-strata_z_transakcji}")
        #     else:
        #         zysk_z_transakcji = abs(after_sell - kapitał) * lewar
        #         zysk = zysk + zysk_z_transakcji
        #         print(f"STOPLOSS Pozycja short otwarta dnia {short_start_data} została zamknięta dnia {df.index[current]}."
        #               f"\n Zysk z transakcji {zysk_z_transakcji}")
        df[f"{company}"][current] = zysk
        companies_earn.loc[companies_earn.index[current], 'zysk'] = companies_earn["zysk"][current].astype(np.float64) + zysk
    companies_earn = companies_earn.join(df[f"{company}"])

fig_zysk = go.Figure(data=go.Scatter(
    # x=df.index, y=df['zysk'], name="k"
                                     ))
for company in companies:
    fig_zysk.add_trace(go.Scatter(
        name=f"{company}",
        mode="lines", x=df.index, y=companies_earn[f'{company}']
))
fig_zysk.add_trace(go.Scatter(
    name="Zysk",
    mode="lines", x=df.index, y=companies_earn['zysk']
))
fig_zysk.update_xaxes(
    rangeslider_visible=True,
    rangebreaks=[
        # NOTE: Below values are bound (not single values), ie. hide x to y
        dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
        # dict(bounds=[18, 9], pattern="hour"),  # hide hours outside of 9.30am-4pm
        # dict(values=["2020-12-25", "2021-01-01"])  # hide holidays (Christmas and New Year's, etc)
    ]
)
fig_zysk.update_layout(
    title='Stock Analysis',
    yaxis_title=f'{company} Stock'
)
fig_zysk.show()
print(f"Zysk ={ret}")
print(f"Procent zyskownych transakcji = {tranzakcje_zyskowne/(tranzakcje_stratne+tranzakcje_zyskowne)}")
