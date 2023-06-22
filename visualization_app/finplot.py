import finplot as fplt
import numpy as np
import pandas as pd
import requests

# pull some data
symbol = 'USDT-BTC'
# url = 'https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName=%s&tickInterval=fiveMin' % symbol
# data = requests.get(url).json()

# format it in pandas
# df = pd.DataFrame(data['result'])
# df = df.rename(columns={'T':'time', 'O':'open', 'C':'close', 'H':'high', 'L':'low', 'V':'volume'})
# df = df.astype({'time':'datetime64[ns]'})

df = pd.read_csv('./visualization_app/amd.csv')

# create three plots
ax,ax2,ax3 = fplt.create_plot(symbol, rows=3)

# plot candle sticks
candle_src = fplt.PandasDataSource(df[['time stamp','open','close','high','low']])
fplt.candlestick_ochl(candle_src, ax=ax)

# put an MA in there
fplt.plot(df['time stamp'], df['close'].rolling(25).mean(), ax=ax, color='#0000ff', legend='ma-25')

# place some dumb markers
hi_wicks = df['high'] - df[['open','close']].T.max().T
df.loc[(hi_wicks>hi_wicks.quantile(0.99)), 'marker'] = df['close']
fplt.plot(df['time stamp'], df['marker'], ax=ax, color='#000000', style='^', legend='dumb mark')

# draw some random crap on our second plot
df['rnd'] = np.random.normal(size=len(df))
fplt.plot(df['time stamp'], df['rnd'], ax=ax2, color='#992277', legend='stuff')
fplt.set_y_range(ax2, -1.4, +1.7) # fix y-axis range

# finally a volume bar chart in our third plot
volume_src = fplt.PandasDataSource(df[['time stamp','open','close','volume']])
fplt.volume_ocv(volume_src, ax=ax3)

# we're done
fplt.show()