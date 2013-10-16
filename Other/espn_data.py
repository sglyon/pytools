"""
Created Mar 5, 2013

Author: Spencer Lyon

Scrape data from espn. Holds ESPN class that has functions for getting
data for various sports, dates, and teams.

see github repo espyn. Not near as good as what this will be, but it
it is a start to look at.
"""
from __future__ import division
import urllib2
import datetime as dt
import pandas as pd
from pandas.io.parsers import TextParser


def _unpack(row, kind='td'):
    els = row.findall('.//%s' % kind)
    return[val.text_content() for val in els]


def _parse_table_data(table):
    rows = table.findall('.//tr')
    header = _unpack(rows[0], kind='th')
    data = [_unpack(r) for r in rows[1:]]
    # Use ',' as a thousands separator as we're pulling from the US site.
    return TextParser(data, names=header, na_values=['N/A'],
                      thousands=',').get_chunk()


class EPSN(object):
    """
    ESPN class that will fetch data from espn.com for a given team,
    sport, and date. In this way the user can uniquely specify an
    exact game they would like to have data for
    """

    def __init__(self):
        self.sports = None
