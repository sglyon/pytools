"""
Created October 12, 2012

Author: Spencer Lyon

Gather all Tickers currently trading on NYSE or NASDAQ
"""
import pandas as pd
import numpy as np
from os.path import basename
from urlparse import urlsplit
import urllib2


def url2name(url):
    return basename(urlsplit(url)[2])


def download(url, localFileName=None):
    localName = url2name(url)
    req = urllib2.Request(url)
    r = urllib2.urlopen(req)
    if 'Content-Disposition' in r:
        # If the response has Content-Disposition, we take file name from it
        localName = r.info()['Content-Disposition'].split('filename=')[1]
        if localName[0] == '"' or localName[0] == "'":
            localName = localName[1:-1]
    elif r.url != url:
        # if we were redirected, the real file name we take from the final URL
        localName = url2name(r.url)
    if localFileName:
        # we can force to save the file as specified name
        localName = localFileName
    f = open(localName, 'wb')
    f.write(r.read())
    f.close()
    return


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
    download(str(first_half + second_half), localFileName=fileName)
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
    download(str(first_half + second_half), localFileName=fileName)
    return
