from __future__ import division
import pandas as pd
import numpy as np
from pandas.io.parsers import ExcelWriter

pd.set_printoptions(max_rows=1000, max_columns=20)


def simple_vol(ticker):
    import datetime as dt
    import pandas.io.data as data

    now = dt.datetime.now()
    month = now.month
    year = now.year
    day = now.day

    sstart = str(month) + '/' + str(day) + '/' + str(year - 1)
    eend = str(month) + '/' + str(day) + '/' + str(year)

    yahoo = data.get_data_yahoo(ticker, start=sstart, end=eend)
    price = yahoo['Adj Close']

    return price.std() / price.mean()


def volatility(ticker):
    """
    Compute the annual and monthly volatilty of a stock given its
    ticker.

    Parameters
    ----------
    ticker: str
        The ticker of the stock you would like to use

    Returns
    -------
    ann_vol: float
        The annual volatility of the stock

    month_vol: float
        The monthly volatility of the stock.
    """
    import numpy as np
    import datetime as dt
    import pandas.io.data as data

    now = dt.datetime.now()
    month = now.month
    year = now.year
    day = now.day

    sstart = str(month) + '/' + str(day) + '/' + str(year - 1)
    eend = str(month) + '/' + str(day) + '/' + str(year)

    yahoo = data.get_data_yahoo(ticker, start=sstart, end=eend)
    price = yahoo['Adj Close']
    num_days = price.size

    returns = price.pct_change() + 1.
    log_returns = np.log(returns) ** 2.
    ann_volaltilty = (log_returns.std(ddof=1) / log_returns.mean())
    ann_volaltilty /= np.sqrt(1. / num_days)
    monthly_volatilty = ann_volaltilty * np.sqrt(1. / 12)

    return [ann_volaltilty, monthly_volatilty]

# nasdaq_file = pd.io.parsers.ExcelFile('NASDAQ_covered_call.xlsx')
# df = nasdaq_file.parse('Covered Call')
# df['Market'] = 'NASDAQ'
# nyse_file = pd.io.parsers.ExcelFile('NYSE_covered_call.xlsx')
# df2 = nyse_file.parse('Covered Call')
# df2['Market'] = 'NYSE'
# df3 = pd.concat([df, df2])
# ticks = df3.Ticker.unique()

# # Find volatility and add a column for it
# vols = dict([(i, simple_vol(i)) for i in ticks])
# df3['Volatility'] = df3['Ticker'].map(vols)

# # We want some returns
# more_than_7 = df3[df3['Annual Return'] > 0.07]

# # Change index
# more_than_7 = more_than_7.set_index('Ticker')

# # Properly create and sort multi-index df
# multi = df3.set_index(['Industry', 'Ticker'])
# multi = multi.sort('Annual Return', ascending=0).sort_index()

# # Sort stuff and keep only lines where industry is known.
# sorts = more_than_7.sort_index(by=['Industry', 'Annual Return'],
#                                  ascending=False)
# sorts = sorts[sorts.Industry != 'n/a']

# industries = np.array(sorts['Industry'].unique(), dtype=str)

# file_name = 'Combined_Volatility.xlsx'
# writer = ExcelWriter(file_name)
# sorts.to_excel(writer, sheet_name='All')
# writer.save()
re_order_cols = ['Name', 'Industry', 'Sector', 'Market Cap', 'Strike',
                 'Exp. Date', 'Option Volume', 'Option Price', 'Stock Price',
                 'Ex. Div Date', 'Num Divs.', 'Div/share', 'Div Inc',
                 'Gain/Loss Exercise', 'Total Income', 'Return',
                 'Annual Return', 'Market', 'Volatility',
                 'Div per Share / Price']

combined_file = pd.io.parsers.ExcelFile('Combined_Volatility.xlsx')
df = combined_file.parse('All')
sorts = df.set_index('Ticker')
only_divs = sorts[sorts['Ex. Div Date'] != 'None']
stable = only_divs[only_divs.Volatility <= 0.08]
close = stable[np.abs(stable['Gain/Loss Exercise']) <= 1]
close['Div per Share / Price'] = close['Div/share'] / close['Stock Price']
highest = close['Div per Share / Price'].argsort()[::-1]

re_order_cols = ['Name', 'Industry', 'Sector', 'Market Cap', 'Stock Price',
                 'Strike', 'Exp. Date', 'Option Volume', 'Option Price',
                 'Ex. Div Date', 'Num Divs.', 'Div/share', 'Div Inc',
                 'Gain/Loss Exercise', 'Total Income', 'Return',
                 'Annual Return', 'Market', 'Volatility',
                 'Div per Share / Price']

close = close[re_order_cols]
