"""
Created Feb 6, 2013

Author: Spencer Lyon

File to be run automatically by cron each day to gather options data
"""
import urllib
import datetime as dt
import pandas as pd
import numpy as np
from options import Options
import h5py as h5


def ticker_series():
    """
    Downloads a .csv file with all tickers in both the nyse and the
    nasdaq. It then puts this info in a pandas Series.

    Parameters
    ----------
    None

    Returns
    -------
    ser: pd.Series
        A pandas Series containing all tickers on the nyse and nasdaq
        exchanges, sorted in alphabetical order.
    """
    nas_file_name = 'nasdaq_tickers.csv'
    nas_first_half = 'http://www.nasdaq.com/screening/companies-by-name.aspx'
    nas_second_half = '?letter=0&exchange=nasdaq&render=download'
    nas_total = nas_first_half + nas_second_half
    urllib.urlretrieve(nas_total, nas_file_name)

    ny_file_name = 'nyse_tickers.csv'
    ny_first_half = 'http://www.nasdaq.com/screening/companies-by-name.aspx'
    ny_second_half = '?letter=0&exchange=nyse&render=download'
    ny_total = ny_first_half + ny_second_half
    urllib.urlretrieve(ny_total, ny_file_name)

    df_nas = pd.read_csv(nas_file_name)
    df_ny = pd.read_csv(ny_file_name)
    df = pd.concat([df_ny, df_nas])
    ser = df.sort('Symbol').Symbol
    ser = ser.reset_index()
    ser = ser['Symbol']

    return ser

tickers = ticker_series()  # Get tickers
num_ticks = tickers.size

months = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
          7: 'Jul', 8: 'Aug', 9: 'Se[', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

now = dt.datetime.now()  # Get current time
c_month = months[now.month]  # Get current month
c_day = str(now.day)  # Get current day
c_year = str(now.year)  # Get current year

f = h5.File('/Volumes/Secondary HD/options_db.h5')  # open database file
year = f.require_group(c_year)  # Make hdf5 group for year
month = year.require_group(c_month)  # Make hdf5 group for month
day = month.require_group(c_day)  # Make hdf5 group for day

num = 0
for i in tickers:
    option = Options(i)

    # NOTE: this functionality is forthcoming in pandas 0.11
    raw_calls = option.get_forward_data(months=3, call=1, put=0,
                                        near=1, above_below=6)
    raw_puts = option.get_forward_data(months=3, call=0, put=1,
                                        near=1, above_below=6)

    if raw_calls.values.any():  # Check if any calls were returned
        try:  # Try to add item to file.
            expiries = raw_calls.Expiry.unique().astype(str)  # get unique expiries
            tick = day.require_group(i)  # make/retrieve hdf5 group for ticker

            for ex in expiries:  # Handle this one expiry at at time
                data = raw_calls[raw_calls.Expiry == ex]  # pull out data for expiry
                i_calls = data[['Strike', 'Last', 'Vol']]  # only keep a few items
                i_calls.Vol = i_calls.Vol.str.replace(',', '')  # Strip ',' from Vol

                # Create dataset C+TICK+expiry
                ex_m_y = ex[:2] + ex[-3:]  # Get only month, year for name
                call_ds = tick.require_dataset('C' + i + ex_m_y,
                                               i_calls.shape, float)
                call_ds[...] = i_calls.astype(np.float32)  # Populate dataset
        except:  # If it doesn't work just pass
            pass

    if raw_puts.values.any():  # Check if any puts were returned
        try:
            # The logic in this if block is the same as for the calls. Check
            # comments there
            expiries = raw_puts.Expiry.unique().astype(str)
            tick = day.require_group(i)

            for ex in expiries:
                data = raw_puts[raw_puts.Expiry == ex]
                i_puts = data[['Strike', 'Last', 'Vol']]
                i_puts.Vol = i_puts.Vol.str.replace(',', '')
                ex_m_y = ex[:2] + ex[-3:]
                put_ds = tick.require_dataset('P' + i + ex_m_y,
                                              i_puts.shape, float)
                put_ds[...] = i_puts.astype(np.float32)
        except:
            pass

    # status update
    num += 1
    if num % 25 == 0:
        print "just finished %s of %s" % (str(num), str(num_ticks))

f.close()  # Close file
