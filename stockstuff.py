import yfinance as yf
import finplot as fplt

df = yf.download('TSLA',start='2021-10-1', end = '2021-12-25')
fplt.candlestick_ochl(df[['Open','Close','High','Low']])
fplt.plot(df.Close.rolling(50).mean())
fplt.plot(df.Close.rolling(200).mean())
fplt.show()
#%% 

#JKSHDSKJHWUIEYWEKJSHDRUIY

import yfinance as yf
import finplot as fplt
import pandas as pd
import requests
from io import StringIO
from time import time
import numpy as np
import tkinter as tk
from tkinter import simpledialog

ROOT = tk.Tk()
##adding more function from user input la
ROOT.withdraw()
# the input dialog
USER_INP = simpledialog.askstring(title="Stocks",
                                  prompt="Which Ticker?:")

symbol = USER_INP
interval_1 = '5m'
interval = '5m'


df = yf.download(  # or pdr.get_data_yahoo(...
        # tickers list or string as well
        tickers = symbol,

        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        period = "1mo",
        #start = '2021-03-30',
        #end = '2021-04-01',

        # fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        interval = interval_1,

        # Whether to ignore timezone when aligning ticker data from 
        # different timezones. Default is True. False may be useful for 
        # minute/hourly data.
        ignore_tz = False,

        # group by ticker (to access via data['SPY'])
        # (optional, default is 'column')
        group_by = 'ticker',

        # adjust all OHLC automatically
        # (optional, default is False)
        auto_adjust = True,

        # attempt repair of missing data or currency mixups e.g. $/cents
        repair = False,

        # download pre/post regular market hours data
        # (optional, default is False)
        prepost = True,

        # use threads for mass downloading? (True/False/Integer)
        # (optional, default is True)
        threads = True,

        # proxy URL scheme use use when downloading?
        # (optional, default is None)
        proxy = None
    )


df['dates'] = df.index
df['Date'] = df.index.astype(np.int64)
df = df.loc[:,['Date','Open','High','Low','Close','Volume','dates']]
df = df.reset_index(drop=True)

ax,ax2 = fplt.create_plot(symbol, rows=2)




# plot price and volume
fplt.candlestick_ochl(df[['Date','Open','Close','High','Low']], ax=ax)
hover_label = fplt.add_legend('', ax=ax)
axo = ax.overlay()
fplt.volume_ocv(df[['Date','Open','Close','Volume']], ax=axo)
fplt.plot(df.Volume.ewm(span=24).mean(), ax=axo, color=1)


#######################################################
## update crosshair and legend when moving the mouse ##

def plot_rsi(df, ax):
    diff = df.Close.diff().values
    gains = diff
    losses = -diff
    with np.errstate(invalid='ignore'):
        gains[(gains<0)|np.isnan(gains)] = 0.0
        losses[(losses<=0)|np.isnan(losses)] = 1e-10 # we don't want divide by zero/NaN
    n = 14
    m = (n-1) / n
    ni = 1 / n
    g = gains[n] = np.nanmean(gains[:n])
    l = losses[n] = np.nanmean(losses[:n])
    gains[:n] = losses[:n] = np.nan
    for i,v in enumerate(gains[n:],n):
        g = gains[i] = ni*v + m*g
    for i,v in enumerate(losses[n:],n):
        l = losses[i] = ni*v + m*l
    rs = gains / losses
    df['rsi'] = 100 - (100/(1+rs))
    df.rsi.plot(ax=ax, legend='RSI')
    fplt.set_y_range(0, 100, ax=ax)
    fplt.add_band(30, 70, ax=ax, color = '#242320')


def update_legend_text(x, y):
    row = df.loc[df.Date==x]
    # format html with the candle and set legend
    fmt = '<span style="color:#%s">%%.2f</span>' % ('0b0' if (row.Open<row.Close).all() else 'a00')
    rawtxt = '<span style="font-size:24px">%%s %%s</span> &nbsp; O%s C%s H%s L%s' % (fmt, fmt, fmt, fmt)
    hover_label.setText(rawtxt % (symbol, interval.upper(), row.Open, row.Close, row.High, row.Low))

def update_crosshair_text(x, y, xtext, ytext):
    ytext = '%s (Close%+.2f)' % (ytext, (y - df.iloc[x].Close))
    return xtext, ytext

fplt.set_time_inspector(update_legend_text, ax=ax, when='hover')
fplt.add_crosshair_info(update_crosshair_text, ax=ax)

price_range = max(df['High']) - min(df['Low'])
date_range = len(df)
fplt.add_text((df['dates'][int(np.floor(date_range/2))], max(df['High']) - price_range/2), str(symbol), color='#bb7700')

plot_rsi(df, ax2)

fplt.show()


#%%
##TESTING GROUND
