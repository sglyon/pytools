import urllib2
from pandas import DataFrame, concat
from pandas.io.parsers import TextParser
import datetime as dt
from pandas.io.data import get_quote_yahoo
import numpy as np

# Items needed for options class
cur_month = dt.datetime.now().month
cur_year = dt.datetime.now().year


def _unpack(row, kind='td'):
    els = row.findall('.//%s' % kind)
    return[val.text_content() for val in els]


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

    # Can now access aapl.calls instance variable
    >>> aapl.calls

    # Fetch September 2012 put data
    >>> puts = aapl.get_put_data(9, 2012)

    # Can now access aapl.puts instance variable
    >>> aapl.puts

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
        month: number, int, optional(default=None)
            The month the options expire. This should be either 1 or 2
            digits.

        year: number, int, optional(default=None)
            The year the options expire. This sould be a 4 digit int.


        Returns
        -------
        call_data: pandas.DataFrame
            A DataFrame with call options data.

        put_data: pandas.DataFrame
            A DataFrame with call options data.


        Notes
        -----
        When called, this function will add instance variables named
        calls and puts. See the following example:

            >>> aapl = Options('aapl')  # Create object
            >>> aapl.calls  # will give an AttributeError
            >>> aapl.get_options_data()  # Get data and set ivars
            >>> aapl.calls  # Doesn't throw AttributeError

        Also note that aapl.calls and appl.puts will always be the calls
        and puts for the next expiry. If the user calls this method with
        a different month or year, the ivar will be named callsMMYY or
        putsMMYY where MM and YY are, repsectively, two digit
        representations of the month and year for the expiry of the
        options.
        """
        from lxml.html import parse

        if month and year:  # try to get specified month from yahoo finance
            m1 = month if len(str(month)) == 2 else '0' + str(month)
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

        if month:
            c_name = 'calls' + str(m1) + str(year)[2:]
            p_name = 'puts' + str(m1) + str(year)[2:]
            self.__setattr__(c_name, call_data)
            self.__setattr__(p_name, put_data)
        else:
            self.calls = call_data
            self.calls = put_data

        return [call_data, put_data]

    def get_call_data(self, month=None, year=None):
        """
        Gets call/put data for the stock with the expiration data in the
        given month and year

        Parameters
        ----------
        month: number, int, optional(default=None)
            The month the options expire. This should be either 1 or 2
            digits.

        year: number, int, optional(default=None)
            The year the options expire. This sould be a 4 digit int.

        Returns
        -------
        call_data: pandas.DataFrame
            A DataFrame with call options data.

        Notes
        -----
        When called, this function will add instance variables named
        calls and puts. See the following example:

            >>> aapl = Options('aapl')  # Create object
            >>> aapl.calls  # will give an AttributeError
            >>> aapl.get_call_data()  # Get data and set ivars
            >>> aapl.calls  # Doesn't throw AttributeError

        Also note that aapl.calls will always be the calls for the next
        expiry. If the user calls this method with a different month
        or year, the ivar will be named callsMMYY where MM and YY are,
        repsectively, two digit representations of the month and year
        for the expiry of the options.
        """
        from lxml.html import parse

        if month and year:  # try to get specified month from yahoo finance
            m1 = month if len(str(month)) == 2 else '0' + str(month)
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

        if month:
            name = 'calls' + str(m1) + str(year)[2:]
            self.__setattr__(name, call_data)
        else:
            self.calls = call_data

        return call_data

    def get_put_data(self, month=None, year=None):
        """
        Gets put data for the stock with the expiration data in the
        given month and year

        Parameters
        ----------
        month: number, int, optional(default=None)
            The month the options expire. This should be either 1 or 2
            digits.

        year: number, int, optional(default=None)
            The year the options expire. This sould be a 4 digit int.

        Returns
        -------
        put_data: pandas.DataFrame
            A DataFrame with call options data.

        Notes
        -----
        When called, this function will add instance variables named
        puts. See the following example:

            >>> aapl = Options('aapl')  # Create object
            >>> aapl.puts  # will give an AttributeError
            >>> aapl.get_put_data()  # Get data and set ivars
            >>> aapl.puts  # Doesn't throw AttributeError

                    return self.__setattr__(self, str(str(x) + str(y)))

        Also note that aapl.puts will always be the puts for the next
        expiry. If the user calls this method with a different month
        or year, the ivar will be named putsMMYY where MM and YY are,
        repsectively, two digit representations of the month and year
        for the expiry of the options.
        """
        from lxml.html import parse

        if month and year:  # try to get specified month from yahoo finance
            m1 = month if len(str(month)) == 2 else '0' + str(month)
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

        if month:
            name = 'puts' + str(m1) + str(year)[2:]
            self.__setattr__(name, put_data)
        else:
            self.puts = put_data

        return put_data

    def get_near_stock_price(self, above_below=2, call=True, put=False,
                             month=None, year=None):
        """
        Cuts the data frame opt_df that is passed in to only take
        options that are near the current stock price.

        Parameters
        ----------
        above_below: number, int, optional (default=2)
            The number of strike prices above and below the stock price that
            should be taken

        call: bool
            Tells the function weather or not it should be using
            self.calls

        put: bool
            Tells the function weather or not it should be using
            self.puts

        month: number, int, optional(default=None)
            The month the options expire. This should be either 1 or 2
            digits.

        year: number, int, optional(default=None)
            The year the options expire. This sould be a 4 digit int.

        Returns
        -------
        chopped: DataFrame
            The resultant DataFrame chopped down to be 2 * above_below + 1 rows
            desired. If there isn't data as far out as the user has asked for
            then
        """
        price = float(get_quote_yahoo([self.symbol])['last'])

        if call:
            try:
                if month:
                    m1 = month if len(str(month)) == 2 else '0' + str(month)
                    name = 'calls' + str(m1) + str(year)[2:]
                    df_c = self.__getattribute__(name)
                else:
                    df_c = self.calls
            except AttributeError:
                df_c = self.get_call_data(month, year)

            # NOTE: For some reason the put commas in all values >1000. We remove
            #       them here
            df_c.Strike = df_c.Strike.astype(str).apply(lambda x: \
                                                        x.replace(',', ''))
            # Now make sure Strike column has dtype float
            df_c.Strike = df_c.Strike.astype(float)

            start_index = np.where(df_c['Strike'] > price)[0][0]

            get_range = range(start_index - above_below,
                              start_index + above_below + 1)

            chop_call = df_c.ix[get_range, :]

            chop_call = chop_call.dropna()
            chop_call = chop_call.reset_index()

        if put:
            try:
                if month:
                    m1 = month if len(str(month)) == 2 else '0' + str(month)
                    name = 'puts' + str(m1) + str(year)[2:]
                    df_p = self.__getattribute__(name)
                else:
                    df_p = self.puts
            except AttributeError:
                df_p = self.get_put_data(month, year)

            # NOTE: For some reason the put commas in all values >1000. We remove
            #       them here
            df_p.Strike = df_p.Strike.astype(str).apply(lambda x: \
                                                        x.replace(',', ''))
            # Now make sure Strike column has dtype float
            df_p.Strike = df_p.Strike.astype(float)

            start_index = np.where(df_p.Strike > price)[0][0]

            get_range = range(start_index - above_below,
                              start_index + above_below + 1)

            chop_put = df_p.ix[get_range, :]

            chop_put = chop_put.dropna()
            chop_put = chop_put.reset_index()

        if call and put:
            return [chop_call, chop_put]
        else:
            if call:
                return chop_call
            else:
                return chop_put

    def get_forward_data(self, months, call=True, put=False, near=False,
                         above_below=2):
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

        near: bool, optional (default=False)
            Whether this function should get only the data near the
            current stock price. Uses Options.get_near_stock_price

        above_below: number, int, optional (default=2)
            The number of strike prices above and below the stock price that
            should be taken if the near option is set to True

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
        in_years = [cur_year] * (months + 1)

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
                m2 = in_months[mon]
                y2 = in_years[mon]
                try:  # This catches cases when there isn't data for a month
                    if not near:
                        try:  # Try to access the ivar if already instantiated

                            m1 = m2 if len(str(m2)) == 2 else '0' + str(m2)
                            name = 'calls' + str(m1) + str(y2)[2:]
                            call_frame = self.__getattribute__(name)
                        except:
                            call_frame = self.get_call_data(in_months[mon],
                                                        in_years[mon])

                    else:
                        call_frame = self.get_near_stock_price(call=True,
                                                               put=False,
                                                    above_below=above_below,
                                                    month=m2, year=y2)

                    tick = str(call_frame.Symbol[0])
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
                m2 = in_months[mon]
                y2 = in_years[mon]
                try:  # This catches cases when there isn't data for a month
                    if not near:
                        try:  # Try to access the ivar if already instantiated

                            m1 = m2 if len(str(m2)) == 2 else '0' + str(m2)
                            name = 'puts' + str(m1) + str(y2)[2:]
                            put_frame = self.__getattribute__(name)
                        except:
                            put_frame = self.get_call_data(in_months[mon],
                                                        in_years[mon])

                    else:
                        put_frame = self.get_near_stock_price(call=False,
                                                              put=True,
                                                    above_below=above_below,
                                                    month=m2, year=y2)

                    # Add column with expiry data to this frame.
                    tick = str(put_frame.Symbol[0])
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
