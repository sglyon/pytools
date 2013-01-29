"""
Created Jan 25, 2013

Author: Spencer Lyon

Collect data for a standard covered call stock option play.

The covered call is very simple and consists of two actions.
    1. I go long in an equity
    2. I write (sell) a call

The writing of the call serves as a hedge against the stock price
falling too low.

In this implementation I make one (somewhat strong) assumption: the
stock price will be equal to the strike price upon expiry of the option.
"""
from __future__ import division
import numpy as np
import pandas as pd
from pandas.io.parsers import ExcelWriter
from pandas.io.data import Options, get_data_yahoo, _parse_options_data
from yahooStocks import StockInfo
from dateutil import parser
import datetime as dt
import urllib
from lxml.html import parse
import urllib2

pd.set_option('line', 200)

# Define how many months to go out
plus = 6

now = dt.datetime.now()
month = now.month
year = now.year
day = now.day

sstart = str(month) + '/' + str(day) + '/' + str(year - 1)
eend = str(month) + '/' + str(day) + '/' + str(year)


def prep_frame(market):
    """
    Downloads a .csv file with all tickers in either the nyse or the
    nasdaq. It then puts this info in a pandas DataFrame and cleans
    it up a bit.

    Parameters
    ----------
    market: str
        Either nyse or nasdaq based on what you want.

    Returns
    -------
    frame: pd.DataFrame
        The DataFrame with Name, MarketCap, Sector, inudstry, and ticker
        as the index
    """
    if market == 'nasdaq':
        file_name = 'nasdaq_tickers.csv'
        first_half = 'http://www.nasdaq.com/screening/companies-by-name.aspx'
        second_half = '?letter=0&exchange=nasdaq&render=download'
        total = first_half + second_half
        urllib.urlretrieve(total, file_name)

    elif market == 'nyse':
        file_name = 'nyse_tickers.csv'
        first_half = 'http://www.nasdaq.com/screening/companies-by-name.aspx'
        second_half = '?letter=0&exchange=nyse&render=download'
        total = first_half + second_half
        urllib.urlretrieve(total, file_name)

    df = pd.read_csv(file_name)

    frame = df[['Name', 'MarketCap', 'Sector', 'industry']]

    frame.index = df.Symbol

    frame.sort_index(inplace=1)

    return frame


def equity_data(x):
    """
    This is inteded to be passed to DataFrame.apply
    """
    tick = x.name
    stock = StockInfo(tick)

    price = stock.get_price()

    # Compute volatility of given stock
    hist = get_data_yahoo(tick, start=sstart, end=eend)
    history = hist['Adj Close']
    num_days = history.size
    returns = history.pct_change() + 1
    log_returns = np.log(returns) ** 2.
    ann_volaltilty = (log_returns.std(ddof=1) / log_returns.mean())
    ann_volaltilty /= np.sqrt(1. / num_days)
    # monthly_volatilty = ann_volaltilty * np.sqrt(1. / 12)

    try:
        div_date = stock.get_ex_dividend()
        month = parser.parse(div_date).month
        day = parser.parse(div_date).day
        year = parser.parse(div_date).year

        # scrape html to get dividend data
        url = 'http://finance.yahoo.com/q/ks?s=%s+Key+Statistics' % (tick)
        parsed = parse(urllib2.urlopen(url))
        doc = parsed.getroot()
        tables = doc.findall('.//table')
        data = _parse_options_data(tables[28])
        div_share = float(data.ix[1].astype(float))
    except:  # No dividend data
        month = 'NA'
        day = 'NA'
        year = 'NA'
        div_share = np.nan

    x['exdivdate'] = str(str(month) + '-' + str(day) + '-' + str(year))
    x['divmonth'] = month
    x['divday'] = day
    x['divyear'] = year
    x['StockPrice'] = price
    x['DivShare'] = div_share
    x['Volatility'] = ann_volaltilty / price

    return x


def date_range():
    """
    Get current date date and return array 6 months out with shifted
    months/years as nessecary.
    """
    current_month = dt.datetime.now().month
    current_year = dt.datetime.now().year

    months = np.arange(current_month + 1, current_month + plus + 1)
    years = np.ones(6) * current_year

    to_change = 0
    for i in range(len(months)):
        if months[i] > 12:
            months[i] -= 12
            to_change += 1

    for i in range(1, to_change + 1):
        years[-i] += 1

    return months, years


def fill_option_data(frame):
    """
    This collects all call options data near the stock price.

    NOTE
    ----
    If this breaks in the options data it is beacuse I changed the file.
    in my pandas installation. See the class in the local options.py.
    """
    ticks = frame.index

    out = pd.DataFrame()

    for tick in range(1, ticks.size):
        try:
            new = Options(ticks[tick]).get_forward_data(plus, call=True,
                                                        put=False, near=True,
                                                        above_below=2)
            new.index = [ticks[tick]] * new.index.size
            cat = new[['Strike', 'Expiry', 'Last', 'Vol', 'Open Int']]
            out = pd.concat([out, cat])
        except:
            pass

    return out

nas = prep_frame('nasdaq')
nyse = prep_frame('nyse')

big = pd.concat([nyse, nas])
big.sort_index(inplace=1)

industries = big.industry
sectors = big.Sector
tickers = big.index
names = big.Name
market_caps = big.MarketCap

num_tickers = tickers.size

big['exdivdate'] = np.nan
big['divmonth'] = np.nan
big['divday'] = np.nan
big['divyear'] = np.nan
big['StockPrice'] = np.nan
big['DivShare'] = np.nan
big['Volatility'] = np.nan

big = big.apply(equity_data, axis=1)

opts = fill_option_data(big)

big = big.join(opts)

# Get ex dividend dates
divday = big.divday
divmonth = big.divmonth
divyear = big.divyear
next_div_month = divmonth + 3
two_next_div_month = divmonth + 6

# Prepare comparison dates
current_day = dt.datetime.now().day
current_month = dt.datetime.now().month
current_year = dt.datetime.now().year

op_months, op_years = date_range()
abs_op_months = np.arange(current_month + 1, current_month + 1 + plus)

# Create column for num divs
big['NumDivs'] = np.nan
numDivs = np.zeros(divmonth.size)

# Get option expiry data
mat_month = big.Expiry.str[:2].astype(float)
mat_day = big.Expiry.str[3:5].astype(float)


# Loop over all expirations and get num divs
for i in range(divmonth.size):
    current_month = dt.datetime.now().month
    _m_month = mat_month[i]

    _div_year = divyear[i]
    _div_month = divmonth[i]
    _p_div_month = next_div_month[i]
    _2p_div_month = two_next_div_month[i]

    current_month += 12 * (current_year - _div_year)
    _m_month += 12 * (current_year - _div_year)

    if current_month > _div_month:
        if _m_month < _p_div_month:
            numDivs[i] = 0

        elif _m_month >= _p_div_month:
            if _m_month >= _2p_div_month:
                numDivs[i] = 2.
            else:
                numDivs[i] = 1.

    elif current_month < _div_month:
        if _m_month < next_div_month[i]:
            numDivs[i] = 1.

        elif _m_month >= _p_div_month:
            if _m_month >= _2p_div_month:
                numDivs[i] = 3.
            else:
                numDivs[i] = 2.

    elif current_month == _div_month:
        if current_day <= divday[i]:
            if _m_month < next_div_month[i]:
                numDivs[i] = 1.

            elif _m_month >= _p_div_month:
                if _m_month >= _2p_div_month:
                    numDivs[i] = 3.
                else:
                    numDivs[i] = 2.

        elif current_day > divday[i]:
            if _m_month < _p_div_month:
                numDivs[i] = 0

            elif _m_month >= _p_div_month:
                if _m_month >= _2p_div_month:
                    numDivs[i] = 2.
                else:
                    numDivs[i] = 1.

current_month = dt.datetime.now().month

# Set Num divs and remove un-necessary columns
big.NumDivs = numDivs
big = big.drop(['divday', 'divmonth', 'divyear'], axis=1)

# Add dividend income column
big['DivIncome'] = big.NumDivs * big.DivShare

# Add gain/loss exercise column. This assumes stock price is at strike price
# at maturity
big['GLExercise'] = big.Strike - big.StockPrice

# Calculate total income, only include losses in movement of stock price
# when it matures at the strike price
losses = big.GLExercise < 0.0
only_losses = big.GLExercise * losses
big['TotalIncome'] = only_losses + big.DivIncome + big.Last

# Calculate the return over the life of the play and annual return
big['Return'] = big.TotalIncome / big.StockPrice
time_to_mat = mat_month - current_month
big['AnnRet'] = big.Return * (12. / time_to_mat)

today = str(str(dt.datetime.now().month) +
            str(dt.datetime.now().day) +
            str(dt.datetime.now().year))

xlsx = '.xlsx'
csv = '.csv'
file_name = 'All_covered_call' + today

name_xl = file_name + xlsx
name_cs = file_name + csv
writer = ExcelWriter(name_xl)
big.to_excel(writer, sheet_name='Covered Call')
writer.save()

big.to_csv(name_cs)
