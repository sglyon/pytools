"""
Created October 12, 2012

Author: Spencer Lyon

Gather all Tickers currently trading on NYSE or NASDAQ
"""
import urllib


def get_nasdaq(fileName='nasdaq_tickers.csv'):
    """
    Fetches a csv file with all the nasdaq tickers.

    Parameters
    ----------
    fileName: str, optional(default=nasdaq.csv)
        The file name it should be saved under. This is optional

    Returns
    -------
    None

    Notes
    -----
    This function gets the data from the following url:
    http://www.nasdaq.com/screening/companies-by-name.aspx?\
        letter=0&exchange=nasdaq&render=download

    where teh '\' is just to make sure the line is too long (remove it)
    """
    first_half = 'http://www.nasdaq.com/screening/companies-by-name.aspx'
    second_half = '?letter=0&exchange=nasdaq&render=download'
    total = first_half + second_half
    urllib.urlretrieve(total, fileName)
    return


def get_nyse(fileName='nyse_tickers.csv'):
    """
    Fetches a csv file with all the nasdaq tickers.

    Parameters
    ----------
    fileName: str, optional(default=nasdaq.csv)
        The file name it should be saved under. This is optional

    Returns
    -------
    None

    Notes
    -----
    This function gets the data from the following url:
    http://www.nasdaq.com/screening/companies-by-name.aspx?\
        letter=0&exchange=nasdaq&render=download

    where teh '\' is just to make sure the line is too long (remove it)
    """
    first_half = 'http://www.nasdaq.com/screening/companies-by-name.aspx'
    second_half = '?letter=0&exchange=nyse&render=download'
    total = first_half + second_half
    urllib.urlretrieve(total, fileName)
    return
