
acceleration=0.005
maximum=0.1

df['SAR'] = ta.SAR(df['High'].values,
                               df['Low'].values,
                               acceleration, maximum)

linear = go.Figure(data=go.Scatter(x=df.index, y=df['SAR']))
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

kasa = 2000
zysk = 0
position_long = 0
position_short = 0
f = df['SAR'][1]
for index in range(len(df)):
    sar = df['SAR'][index]
    price = df["Close"][index]

    #Short
    if sar > price and df['SAR'][index-1] < price:
        if position_long == 1:
            zysk = zysk + ((price*akcje) - kasa)
            position_long = 0
            print(round(zysk,2), ((price*akcje) - kasa))
        position_short = 1
        akcje = kasa/price
        ck = price

    if sar < price:
        #Close short
        if position_short == 1:
            zysk = zysk + ((price*akcje) - kasa)
            position_short = 0
            print(round(zysk,2), ((price*akcje) - kasa))
        position_long = 1
        akcje = kasa/price
        ck = price

    #takeprofit
    if  position_long == 1 and price*1.03 > ck:
        takeprofit = 1
        zysk = zysk + ((price * akcje) - kasa)
        position_long = 0
        print(round(zysk, 2), ((price * akcje) - kasa))
    elif position_short == 1 and price*0.97 < ck:
        takeprofit = 1
        zysk = zysk + ((price * akcje) - kasa)
        position_short = 0
        print(round(zysk, 2), ((price * akcje) - kasa))