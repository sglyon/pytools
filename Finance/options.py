import urllib2
from pandas import DataFrame, concat
from pandas.io.parsers import TextParser
from datetime import datetime
from pandas.io.data import get_quote_yahoo
import numpy as np

# Items needed for options class
cur_month = dt.datetime.now().month
cur_year = dt.datetime.now().year


def _unpack(row, kind='td'):
    elts = row.findall('.//%s' % kind)
    return[val.text_content() for val in elts]


def _parse_options_data(table):
    rows = table.findall('.//tr')
    header = _unpack(rows[0], kind='th')
    data = [_unpack(r) for r in rows[1:]]
    return TextParser(data, names=header).get_chunk()


class Options(object):
    """
    This class fetches call/put data for a given stock/exipry month.

    It is instantiated with a string representing the ticker symbol.

    The class has the following methods:
        get_options_data:(month, year)
        get_call_data:(month, year)
        get_put_data: (month, year)
        get_near_stock_price(opt_frame, above_below)
        get_forward_data(months, call, put)

    Examples
    --------
    # Instantiate object with ticker
    >>> aapl = Options('aapl')

    # Fetch September 2012 call data
    >>> calls = aapl.get_call_data(9, 2012)

    # Fetch September 2012 put data
    >>> puts = aapl.get_put_data(9, 2012)

    # cut down the call data to be 3 below and 3 above the stock price.
    >>> cut_calls = aapl.get_near_stock_price(calls, above_below=3)

    # Fetch call and put data with expiry from now to 8 months out
    >>> forward_calls, forward_puts = aapl.get_forward_data(8,
        ...                                        call=True, put=True)
    """

    def __init__(self, symbol):
        """ Instantiates options_data with a ticker saved as symbol """
        self.symbol = str(symbol).upper()

    def get_options_data(self, month=None, year=None):
        """
        Gets call/put data for the stock with the expiration data in the
        given month and year

        Parameters
        ----------
        month: number, int
            The month the options expire.

        year: number, int
            The year the options expire.


        Returns
        -------
        call_data: pandas.DataFrame
            A DataFrame with call options data.

        put_data: pandas.DataFrame
            A DataFrame with call options data.
        """
        from lxml.html import parse

        if month and year:  # try to get specified month from yahoo finance
            m1 = month if len(str(month)) == 2 else str('0' + str(month))
            m2 = month

            if m1 != cur_month and m2 != cur_month:  # if this month use other url
                url = str('http://finance.yahoo.com/q/op?s=' + self.symbol +
                          '&m=' + str(year) + '-' + str(m1))

            else:
                url = str('http://finance.yahoo.com/q/op?s=' + self.symbol +
                                                            '+Options')

        else:  # Default to current month
            url = str('http://finance.yahoo.com/q/op?s=' + self.symbol +
                                                            '+Options')

        parsed = parse(urllib2.urlopen(url))
        doc = parsed.getroot()
        tables = doc.findall('.//table')
        calls = tables[9]
        puts = tables[13]

        call_data = _parse_options_data(calls)
        put_data = _parse_options_data(puts)

        self.calls = call_data
        self.puts = put_data

        return [call_data, put_data]

    def get_call_data(self, month=None, year=None):
        """
        Gets call/put data for the stock with the expiration data in the
        given month and year

        Parameters
        ----------
        month: number, int, optional(default=None)
            The month the options expire.

        year: number, int, optional(defaule=None)
            The year the options expire.

        Returns
        -------
        call_data: pandas.DataFrame
            A DataFrame with call options data.
        """
        from lxml.html import parse

        if month and year:  # try to get specified month from yahoo finance
            m1 = month if len(str(month)) == 2 else str('0' + str(month))
            m2 = month

            if m1 != cur_month and m2 != cur_month:  # if this month use other url
                url = str('http://finance.yahoo.com/q/op?s=' + self.symbol +
                          '&m=' + str(year) + '-' + str(m1))

            else:
                url = str('http://finance.yahoo.com/q/op?s=' + self.symbol +
                                                            '+Options')

        else:  # Default to current month
            url = str('http://finance.yahoo.com/q/op?s=' + self.symbol +
                                                            '+Options')

        parsed = parse(urllib2.urlopen(url))
        doc = parsed.getroot()
        tables = doc.findall('.//table')
        calls = tables[9]

        call_data = _parse_options_data(calls)

        self.calls = call_data

        return call_data

    def get_put_data(self, month=None, year=None):
        """
        Gets put data for the stock with the expiration data in the
        given month and year

        Parameters
        ----------
        month: number, int, optional(default=None)
            The month the options expire.

        year: number, int, optional(defaule=None)
            The year the options expire.

        Returns
        -------
        put_data: pandas.DataFrame
            A DataFrame with call options data.
        """
        from lxml.html import parse

        if month and year:  # try to get specified month from yahoo finance
            m1 = month if len(str(month)) == 2 else str('0' + str(month))
            m2 = month

            if m1 != cur_month and m2 != cur_month:  # if this month use other url
                url = str('http://finance.yahoo.com/q/op?s=' + self.symbol +
                          '&m=' + str(year) + '-' + str(m1))

            else:
                url = str('http://finance.yahoo.com/q/op?s=' + self.symbol +
                                                            '+Options')

        else:  # Default to current month
            url = str('http://finance.yahoo.com/q/op?s=' + self.symbol +
                                                            '+Options')

        parsed = parse(urllib2.urlopen(url))
        doc = parsed.getroot()
        tables = doc.findall('.//table')
        puts = tables[13]

        put_data = _parse_options_data(puts)

        self.puts = put_data

        return put_data

    def get_near_stock_price(self, call=True, put=False, above_below=2):
        """
        Cuts the data frame opt_df that is passed in to only take
        options that are near the current stock price.

        Parameters
        ----------
        call: bool
            Tells the function weather or not it should be using
            self.calls

        put: bool
            Tells the function weather or not it should be using
            self.puts

        above_below: number, int, optional (default=2)
            The number of strike prices above and below the stock price that
            should be taken

        Returns
        -------
        chopped: DataFrame
            The resultant DataFrame chopped down to be 2 * above_below + 1 rows
            desired. If there isn't data as far out as the user has asked for
            then
        """
        price = float(get_quote_yahoo([self.symbol])['last'])
        if call == True and put == True:
            raise ValueError('Do either calls or puts, but just one at at time')

        if call == True:
            try:
                opt_df = self.calls
            except AttributeError:
                opt_df = self.get_call_data()
        else:
            try:
                opt_df = self.puts
            except AttributeError:
                opt_df = self.get_put_data()

        start_index = np.where(opt_df['Strike'] > price)[0][0]

        get_range = range(start_index - above_below,
                          start_index + above_below + 1)

        chopped = opt_df.ix[get_range, :]

        chopped = chopped.dropna()
        chopped = chopped.reset_index()

        return chopped

    def get_forward_data(self, months, call=True, put=False):
        """
        Gets either call, put, or both data for months starting in the current
        month and going out in the future a spcified amount of time.

        Parameters
        ----------
        months: number, int
            How many months to go out in the collection of the data. This is
            inclusive.

        call: bool, optional (default=True)
            Whether or not to collect data for call options

        put: bool, optional (default=False)
            Whether or not to collect data for put options.

        Returns
        -------
        all_calls: DataFrame
            If asked for, a DataFrame containing call data from the current
            month to the current month plus months.

        all_puts: DataFrame
            If asked for, a DataFrame containing put data from the current
            month to the current month plus months.
        """
        in_months = range(cur_month, cur_month + months + 1)
        in_years = [cur_year] * months

        # Figure out how many items in in_months go past 12
        to_change = 0
        for i in range(months):
            if in_months[i] > 12:
                in_months[i] -= 12
                to_change += 1

        # Change the corresponding items in the in_years list.
        for i in range(1, to_change + 1):
            in_years[-i] += 1

        if call:
            all_calls = DataFrame()
            for mon in range(months):
                try:  # This catches cases when there isn't data for a month
                    call_frame = self.get_call_data(in_months[mon],
                                                    in_years[mon])
                    tick = str(call_frame.ix[0, 1])
                    start = len(self.symbol)
                    year = tick[start: start + 2]
                    month = tick[start + 2: start + 4]
                    day = tick[start + 4: start + 6]
                    expiry = str(month + '-' + day + '-' + year)
                    call_frame['Expiry'] = expiry
                    if mon == 0:
                        all_calls = all_calls.join(call_frame, how='right')
                    else:
                        all_calls = concat([all_calls, call_frame])
                except:
                    pass

        if put:
            all_puts = DataFrame()
            for mon in range(months):
                try:  # This catches cases when there isn't data for a month
                    put_frame = self.get_put_data(in_months[mon],
                                                  in_years[mon])

                    # Add column with expiry data to this frame.
                    tick = str(put_frame.ix[0, 1])
                    start = len(self.symbol)
                    year = tick[start: start + 2]
                    month = tick[start + 2: start + 4]
                    day = tick[start + 4: start + 6]
                    expiry = str(month + '-' + day + '-' + year)
                    put_frame['Expiry'] = expiry

                    if mon == 0:
                        all_puts = all_puts.join(put_frame, how='right')
                    else:
                        all_puts = concat([all_puts, put_frame])
                except:
                    pass

        if call and put:
            return [all_calls, all_puts]
        else:
            if call:
                return all_calls
            else:
                return all_puts
