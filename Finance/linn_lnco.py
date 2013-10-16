import matplotlib.pyplot as plt
from matplotlib import rcParams
import pandas as pd
from pandas.io.data import get_data_yahoo

plt.ioff()

c1, c2 = rcParams['axes.color_cycle'][:2]

stocks = ['LINE', 'LNCO']
prices = get_data_yahoo(stocks, start='1/1/2000')['Adj Close'].dropna()

day1 = str(prices.index.min().date())
day2 = str(prices.index.max().date())

fig = plt.figure()
ax = fig.add_subplot(111)
prices.plot(ax=ax)
ax.fill_between(prices.index, prices['LINE'], prices['LNCO'], alpha=0.5,
                where=prices['LINE'] >= prices['LNCO'], facecolor=c1)
ax.fill_between(prices.index, prices['LINE'], prices['LNCO'], alpha=0.5,
                where=prices['LINE'] < prices['LNCO'], facecolor=c2)
ax.set_title("LINE and LNCO: %s to %s" % (day1, day2))
ax.set_ylabel('Price')
fig.savefig("/Users/sglyon/Desktop/line_lnco.png", format='png')
plt.show()
