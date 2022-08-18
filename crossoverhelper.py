# importing libs

import pandas as pd
import numpy as np
import numpy
import matplotlib.pyplot as plt
import datetime
import mplfinance as mpf
import ccxt
import tardis_dev
pd.set_option('mode.chained_assignment', None)

# set exch and symbol

exch = ccxt.ftx()
symbol = 'BTC/USDT'

start_time = datetime.datetime.timestamp(datetime.datetime(2020, 3, 25))*1000
time_now = datetime.datetime.timestamp(datetime.datetime.now())*1000
timeframe = '1h'
dfs = []

# get data

while start_time < time_now:
    params = {"endTime": start_time+5000*3600*1000}
    print(params)
    data = exch.fetchOHLCV(symbol, '1h', since=start_time, limit=5000)
    sample = pd.DataFrame(
        data, columns=["time", "open", "high", "low", "close", "volume"])
    sample["time_utc"] = pd.to_datetime(sample.time, unit="ms")
    dfs.append(sample)
    print(start_time)
    print(sample.shape)
    print(sample.time.max())
    print(sample.time.min())
    print(sample.time.max()-sample.time.min())
    print("="*35)
    start_time = sample.time.max()+1

# set up markouts

hours = [1, 2, 4, 12, 24, 48, 240]
hour_cols = [f"future_{str(hour)}" for hour in hours]
df[hour_cols] = pd.concat([df.close.shift(-hour)
                          for hour in hours], axis=1).reset_index(drop=True).values
df = df.loc[df.isna().sum(axis=1) == 0]
df

# crossover calculation

df['close'] = df['close'].astype(float)

periods = [50, 200]
df['fast_sma'] = df['close'].rolling(periods[0]).mean()
df['slow_sma'] = df['close'].rolling(periods[1]).mean()
df['fast_ema'] = df['close'].ewm(span=periods[0], adjust=False).mean()
df['slow_ema'] = df['close'].ewm(span=periods[1], adjust=False).mean()

df['sma_status'] = (df['fast_sma'] > df['slow_sma']).astype(int)
df['ema_status'] = (df['fast_ema'] > df['slow_ema']).astype(int)

df['sma_crossover'] = df['sma_status'].shift(-1) < df['sma_status']
df['ema_crossover'] = df['sma_status'].shift(-1) < df['sma_status']

df['sma_crossunder'] = df['sma_status'].shift(-1) > df['sma_status']
df['ema_crossunder'] = df['sma_status'].shift(-1) > df['sma_status']

# markouts


def log_return(x0, x1):
    return np.log(x1/x0)


def simple_return(x0, x1):
    return ((x1-x0)/x0)


longsma = df[df['sma_crossover'] == True]
shortsma = df[df['sma_crossunder'] == True]
longema = df[df['ema_crossover'] == True]
shortema = df[df['ema_crossunder'] == True]

df['sma_cross'] = df['sma_crossover'] | df['sma_crossunder']
df['ema_cross'] = df['ema_crossover'] | df['ema_crossunder']

LSsma = df[df['sma_cross']].set_index('time_utc')
LSema = df[df['ema_cross']].set_index('time_utc')

df['short'] = df['sma_crossunder'] | df['ema_crossunder']
df['long'] = df['sma_crossover'] | df['ema_crossover']

Shortdf = df[df['short']].set_index('time_utc')
Longdf = df[df['long']].set_index('time_utc')

df['date'] = pd.to_datetime(df['date'], unit='s')

for hour in hours:
    LSema[f'markout_{hour}'] = np.where(LSema['ema_crossover'], simple_return(LSema['close'].astype(
        float), LSema[f'future_{hour}'].astype(float)), simple_return(LSema[f'future_{hour}'].astype(float), LSema['close'].astype(float)))
    LSema[f'log_markout_{hour}'] = np.where(LSema['ema_crossover'], log_return(LSema['close'].astype(
        float), LSema[f'future_{hour}'].astype(float)), log_return(LSema[f'future_{hour}'].astype(float), LSema['close'].astype(float)))
    LSema[f'trade_markout_{hour}'] = LSema[f'markout_{hour}'] * 100
    LSema[f'trade_markout_{hour}'].cumsum().plot(
        legend=True, title='EMA Long/Short Cumulative PnL - $100 per trade')

for i, hour in enumerate(hours):
    plt.figure(i)
    plt.title(f'EMA Long/Short: {hour}h Log Return Markouts')
    LSema[f'log_markout_{hour}'].hist()


for i, hour in enumerate(hours):
    displaylosedf = (LSema.sort_values(by=f'trade_markout_{hour}').head(5))
    display(displaylosedf[[f'trade_markout_{hour}', 'short', 'long']])

LSsma[f'log_markout_{240}'].cumsum().tail(1)[0]
