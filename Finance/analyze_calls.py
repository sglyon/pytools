from __future__ import division
import pandas as pd


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

    returns = price.pct_change()
    log_returns = np.log(returns)
    ann_volaltilty = (log_returns.std() / log_returns.mean())
    ann_volaltilty /= np.sqrt(1. / num_days)
    monthly_volatilty = ann_volaltilty * np.sqrt(1. / 12)

    return [ann_volaltilty, monthly_volatilty]






pd.set_printoptions(max_rows=1000, max_columns=20)

nasdaq_file = pd.io.parsers.ExcelFile('NASDAQ_covered_call.xlsx')
nasdaq = nasdaq_file.parse('Covered Call')
pos_nasdaq = nasdaq[nasdaq['Annual Return'] > 0]

sorts = pos_nasdaq.sort_index(by=['Industry', 'Annual Return'],
                                 ascending=False)
not_na = sorts[sorts.Industry != 'n/a']

industries = []
for i in sorts.Industry.unique():
    industries.append(str(i))
