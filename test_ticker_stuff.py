#DOUBLE AXIS FOR INDICATOR

import yfinance as yf
import finplot as fplt
import pandas as pd
import requests
from io import StringIO
from time import time
import numpy as np

symbol = 'SPY'
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

def update_legend_text(x, y):
    row = df.loc[df.Date==x]
    # format html with the candle and set legend
    fmt = '<span style="color:#%s">%%.2f</span>' % ('0b0' if (row.Open<row.Close).all() else 'a00')
    rawtxt = '<span style="font-size:13px">%%s %%s</span> &nbsp; O%s C%s H%s L%s' % (fmt, fmt, fmt, fmt)
    hover_label.setText(rawtxt % (symbol, interval.upper(), row.Open, row.Close, row.High, row.Low))

def update_crosshair_text(x, y, xtext, ytext):
    ytext = '%s (Close%+.2f)' % (ytext, (y - df.iloc[x].Close))
    return xtext, ytext

fplt.set_time_inspector(update_legend_text, ax=ax, when='hover')
fplt.add_crosshair_info(update_crosshair_text, ax=ax)

price_range = max(df['High']) - min(df['Low'])
date_range = len(df)
fplt.add_text((df['dates'][int(np.floor(date_range/2))], max(df['High']) - price_range/2), str(symbol), color='#bb7700')



fplt.show()
#%% SINGLE AXIS

import yfinance as yf
import finplot as fplt
import pandas as pd
import requests
from io import StringIO
from time import time
import numpy as np
import matplotlib.pyplot as plt

symbol = 'SPY'
time_interval = '5m'



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
        interval = time_interval,

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

## re-structuring df
df['dates'] = df.index
df['Date'] = df.index.astype(np.int64)
df = df.loc[:,['Date','Open','High','Low','Close','Volume','dates']]
df = df.reset_index(drop=True)

ax = fplt.create_plot(symbol)


## plot price and volume
fplt.candlestick_ochl(df[['Date','Open','Close','High','Low']], ax=ax)
hover_label = fplt.add_legend('', ax=ax)
axo = ax.overlay()
fplt.volume_ocv(df[['Date','Open','Close','Volume']], ax=axo)
fplt.plot(df.Volume.ewm(span=24).mean(), ax=axo, color=1)


#######################################################
## update crosshair and legend when moving the mouse ##

def update_legend_text(x, y):
    row = df.loc[df.Date==x]
    # format html with the candle and set legend
    fmt = '<span style="color:#%s">%%.2f</span>' % ('0b0' if (row.Open<row.Close).all() else 'a00')
    rawtxt = '<span style="font-size:13px">%%s %%s</span> &nbsp; O%s C%s H%s L%s' % (fmt, fmt, fmt, fmt)
    hover_label.setText(rawtxt % (symbol, time_interval.upper(), row.Open, row.Close, row.High, row.Low))

def update_crosshair_text(x, y, xtext, ytext):
    ytext = '%s (Close%+.2f)' % (ytext, (y - df.iloc[x].Close))
    return xtext, ytext

fplt.set_time_inspector(update_legend_text, ax=ax, when='hover')
fplt.add_crosshair_info(update_crosshair_text, ax=ax)

## adding ticker text tag
#price_range = max(df['High']) - min(df['Low'])
#date_range = len(df)
#fplt.add_text((df['dates'][int(np.floor(date_range/2))], max(df['High']) - price_range/2), str(symbol), color='#bb7700')

## place some markers on low and high wicks. compares wicks to all other wicks not to price or relative price change
lo_wicks = df[['Open','Close']].T.min() - df['Low']
df.loc[(lo_wicks>lo_wicks.quantile(0.99)), 'marker'] = df['Low']
fplt.plot(df['dates'], df['marker'], ax=ax, color='#4a5', style='^', legend='low wicks')


hi_wicks = df['High'] - df[['Open','Close']].T.max()
df.loc[(hi_wicks>hi_wicks.quantile(0.99)), 'marker2'] = df['High']
fplt.plot(df['dates'], df['marker2'], ax=ax, color='#4a5', style='v', legend='high wicks')

n = len(df)

for i in range(n):
    temp = df['marker'].iloc[i]
    if pd.isnull(df['marker'].iloc[i]) == False:
        fplt.add_line((df['dates'].iloc[0], temp), (df['dates'].iloc[-1], temp), color='#0c8cb2', interactive=False)
        fplt.add_text((df['dates'].iloc[i], temp), str(temp), color='#000000')

for i in range(n):
    temp = df['marker2'].iloc[i]
    if pd.isnull(temp) == False:
        fplt.add_line((df['dates'].iloc[0], temp), (df['dates'].iloc[-1], temp), color='#9900ff', interactive=False)
        fplt.add_text((df['dates'].iloc[i], temp), str(temp), color='#000000')

fplt.show()

#%% SINGLE AXIS

import yfinance as yf
import finplot as fplt
import pandas as pd
import requests
from io import StringIO
from time import time
import numpy as np
import matplotlib.pyplot as plt

symbol = 'SPY'
time_interval = '5m'



df = yf.download(  # or pdr.get_data_yahoo(...
        # tickers list or string as well
        tickers = symbol,

        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        period = "1d",
        #start = '2022-12-21',
        #end = '2022-12-23',

        # fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        interval = time_interval,

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

## re-structuring df
df['dates'] = df.index
df['Date'] = df.index.astype(np.int64)
df = df.loc[:,['Date','Open','High','Low','Close','Volume','dates']]
df = df.reset_index(drop=True)

ax = fplt.create_plot(symbol)


## plot price and volume
fplt.candlestick_ochl(df[['Date','Open','Close','High','Low']], ax=ax)
hover_label = fplt.add_legend('', ax=ax)
axo = ax.overlay()
fplt.volume_ocv(df[['Date','Open','Close','Volume']], ax=axo)
fplt.plot(df.Volume.ewm(span=24).mean(), ax=axo, color=1)


#######################################################
## update crosshair and legend when moving the mouse ##

def update_legend_text(x, y):
    row = df.loc[df.Date==x]
    # format html with the candle and set legend
    fmt = '<span style="color:#%s">%%.2f</span>' % ('0b0' if (row.Open<row.Close).all() else 'a00')
    rawtxt = '<span style="font-size:13px">%%s %%s</span> &nbsp; O%s C%s H%s L%s' % (fmt, fmt, fmt, fmt)
    hover_label.setText(rawtxt % (symbol, time_interval.upper(), row.Open, row.Close, row.High, row.Low))

def update_crosshair_text(x, y, xtext, ytext):
    ytext = '%s (Close%+.2f)' % (ytext, (y - df.iloc[x].Close))
    return xtext, ytext

fplt.set_time_inspector(update_legend_text, ax=ax, when='hover')
fplt.add_crosshair_info(update_crosshair_text, ax=ax)


fib_ratios = [0, 0.236, 0.382, 0.50, 0.618,0.786, 1, 1.618, 2.00, 2.618]

    
df['hour'] = pd.to_datetime(df['dates'].astype(str)).dt.hour
df['min'] = pd.to_datetime(df['dates'].astype(str)).dt.minute

n = len(df)

fib_starts = []
fib_ends = []

for i in range(n):
    if (df['hour'].iloc[i] == 8 and df['min'].iloc[i] == 0):
        fib_starts.append(i)
    if (df['hour'].iloc[i] == 16 and df['min'].iloc[i] == 0):   
        fib_ends.append(i)

m = len(fib_starts)
remeasurement_threshholds = []
for i in range(m):
    start_pt = fib_starts[i]
    H = df['High'].iloc[start_pt]
    L = df['Low'].iloc[start_pt]
    Uptrend_retracement = []
    Uptrend_extension = []
    Downtrend_retracement = []
    Downtrend_extension = []
    for j in fib_ratios:
        Uptrend_retracement.append(H - ((H-L)*j))
        Uptrend_extension.append(H + ((H-L)*j))
        Downtrend_retracement.append(L + ((H-L)*j))
        Downtrend_extension.append(L - ((H-L)*j))
    for k in Uptrend_retracement:
        fplt.add_line((df['dates'].iloc[start_pt], k), (df['dates'].iloc[fib_ends[i]], k), color='#9900ff', interactive=False)
    for k in Downtrend_retracement:
        fplt.add_line((df['dates'].iloc[start_pt], k), (df['dates'].iloc[fib_ends[i]], k), color='#9900ff', interactive=False)
    remeasurement_threshholds.append(Uptrend_retracement[-1])
    #fplt.add_text((df['dates'].iloc[i], temp), str(temp), color='#000000')
    
    #for breaking lines, recalculate based on mins and maxes
    if df['High'][fib_starts[i]:fib_ends[i]].T.max() > Downtrend_retracement[-1]:
        temp_num = df['High'][fib_starts[i]:fib_ends[i]] > Downtrend_retracement[-1]
        temp_num_1 = temp_num[temp_num == True].index[0]

        
    start_pt = fib_starts[i]
    H = df['High'].iloc[temp_num_1]
    L = df['Low'].iloc[start_pt]
    Uptrend_retracement = []
    Uptrend_extension = []
    Downtrend_retracement = []
    Downtrend_extension = []
    for j in fib_ratios:
        Uptrend_retracement.append(H - ((H-L)*j))
        Uptrend_extension.append(H + ((H-L)*j))
        Downtrend_retracement.append(L + ((H-L)*j))
        Downtrend_extension.append(L - ((H-L)*j))
    #for k in Uptrend_retracement:
        #fplt.add_line((df['dates'].iloc[start_pt], k), (df['dates'].iloc[temp_num_1], k), color='#FFA500', interactive=False)
    for k in Downtrend_retracement:
        fplt.add_line((df['dates'].iloc[start_pt], k), (df['dates'].iloc[temp_num_1], k), color='#FFA500', interactive=False)

    
fplt.show()
#%%
notable_wicks = pd.concat([df[df['marker'].notnull()]['marker'], df[df['marker2'].notnull()]['marker2']])
notable_wicks = notable_wicks.sort_index()
wicks_plot = plt.plot(notable_wicks.index, notable_wicks.values)
#%%
from tradingview_ta import TA_Handler, Interval, Exchange

tesla = TA_Handler(
    symbol="TSLA",
    screener="america",
    exchange="NASDAQ",
    interval=Interval.INTERVAL_1_DAY
)
print(tesla.get_analysis().summary)