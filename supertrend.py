
import pandas as pd
pd.set_option('display.max_rows', None)

import warnings
warnings.filterwarnings('ignore')
import pickle
import os

import numpy as np
from datetime import datetime
import time
import math
import threading

def tr(data):
    data['previous_close'] = data['Close'].shift(1)
    data['high-low'] = abs(data['High'] - data['Low'])
    data['high-pc'] = abs(data['High'] - data['previous_close'])
    data['low-pc'] = abs(data['Low'] - data['previous_close'])

    tr = data[['high-low', 'high-pc', 'low-pc']].max(axis=1)

    return tr


def atr(data, period=14):
    data['tr'] = tr(data)
    atr = data['tr'].rolling(period).mean()

    return atr


def supertrend(df, period=12, atr_multiplier=3, period2=10, atr_multiplier2=1, period3=11, atr_multiplier3=2):
    hl2 = (df['High'] + df['Low']) / 2
    df['atr'] = atr(df, period)
    df['upperband'] = hl2 + (atr_multiplier * df['atr'])
    df['lowerband'] = hl2 - (atr_multiplier * df['atr'])

    df['atr2'] = atr(df, period2)
    df['upperband2'] = hl2 + (atr_multiplier2 * df['atr2'])
    df['lowerband2'] = hl2 - (atr_multiplier2 * df['atr2'])

    df['atr3'] = atr(df, period3)
    df['upperband3'] = hl2 + (atr_multiplier3 * df['atr3'])
    df['lowerband3'] = hl2 - (atr_multiplier3 * df['atr3'])
    df['in_uptrend'] = True
    df['in_uptrend2'] = True
    df['in_uptrend3'] = True
    df['uptrend'] = True
    df['ewma'] = df['Close'].ewm(200, adjust=True).mean()

    for current in range(1, len(df.index)):
        previous = current - 1

        if df['Close'][current] > df['upperband'][previous]:
            df['in_uptrend'][current] = True

        elif df['Close'][current] < df['lowerband'][previous]:
            df['in_uptrend'][current] = False

        else:
            df['in_uptrend'][current] = df['in_uptrend'][previous]

            if df['in_uptrend'][current] and df['lowerband'][current] < df['lowerband'][previous]:
                df['lowerband'][current] = df['lowerband'][previous]
            if not df['in_uptrend'][current] and df['upperband'][current] > df['upperband'][previous]:
                df['upperband'][current] = df['upperband'][previous]

        if df['Close'][current] > df['upperband2'][previous]:
            df['in_uptrend2'][current] = True

        elif df['Close'][current] < df['lowerband2'][previous]:
            df['in_uptrend2'][current] = False

        else:
            df['in_uptrend2'][current] = df['in_uptrend2'][previous]

            if df['in_uptrend2'][current] and df['lowerband2'][current] < df['lowerband2'][previous]:
                df['lowerband2'][current] = df['lowerband2'][previous]
            if not df['in_uptrend2'][current] and df['upperband2'][current] > df['upperband2'][previous]:
                df['upperband2'][current] = df['upperband2'][previous]

        if df['Close'][current] > df['upperband3'][previous]:
            df['in_uptrend3'][current] = True

        elif df['Close'][current] < df['lowerband3'][previous]:
            df['in_uptrend3'][current] = False

        else:
            df['in_uptrend3'][current] = df['in_uptrend3'][previous]

            if df['in_uptrend3'][current] and df['lowerband3'][current] < df['lowerband3'][previous]:
                df['lowerband3'][current] = df['lowerband3'][previous]

            if not df['in_uptrend3'][current] and df['upperband3'][current] > df['upperband3'][previous]:
                df['upperband3'][current] = df['upperband3'][previous]

        if df['in_uptrend'][current] and df['in_uptrend2'][current] and df['in_uptrend3'][current]:
            df['uptrend'][current] = True

        else:
            df['uptrend'][current] = False
    return df