from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
from pandas.io.parsers import TextParser, ExcelWriter
from datetime import datetime
from pandas.io.data import get_quote_yahoo
import numpy as np
import pandas as pd

cur_month = datetime.now().month
cur_year = datetime.now().year


def _unpack(row, kind='td'):
    return [val.text for val in row.findAll(kind)]


def _parse_options_data(table):
    rows = table.findAll('tr')
    header = _unpack(rows[0], kind='th')
    data = [_unpack(r) for r in rows[1:]]
    return TextParser(data, names=header).get_chunk()


class Options():
    """
    This class fetches call/put data for a given stock/expiration month.

    It is instantiated with a string representing the ticker symbol.

    The class has the following methods:
        get_options_data:(month, year)
        get_call_data:(month, year)
        get_pu_data: (month, year)
    """

    def __init__(self, symbol):
        """ Instantiates options_data with a ticker saved as symbol """
        self.symbol = str(symbol).upper()

    def get_options_data(self, month=cur_month, year=cur_year, excel=False):
        """
        Gets call/put data for the stock with the expiration data in the
        given month and year

        Parameters
        ----------
        month: number, int
            The month of the options expire.

        year: number, int
            The year the options expire.

        excel: bool, optional(default=False)
            A boolean value indicating whether or not the data should be saved
            to an excel spreadsheet. If true the name of the file will be
            "'ticker'_options.xlsx" unless otherwise indicated. Also there will
            be two sheets created. The first one is named 'calls' and contains
            the call data and the second is for the puts.

        Returns
        -------
        call_data: pandas.DataFrame
            A DataFrame with call options data.

        put_data: pandas.DataFrame
            A DataFrame with call options data.
        """

        mon_in = month if len(str(month)) == 2 else str('0' + str(month))

        url = str('http://finance.yahoo.com/q/op?s=' + self.symbol + '&m=' +
                  str(year) + '-' + str(mon_in))

        buf = urlopen(url)
        soup = BeautifulSoup(buf)
        body = soup.body

        tables = body.findAll('table')
        calls = tables[9]
        puts = tables[13]

        call_data = _parse_options_data(calls)
        put_data = _parse_options_data(puts)

        if excel == True:
            file_name = str(str(self.symbol).upper() + '_options.xlsx')
            writer = ExcelWriter(file_name)
            put_data.to_excel(writer, sheet_name='puts')
            call_data.to_excel(writer, sheet_name='calls')
            writer.save()

        return [call_data, put_data]

    def get_call_data(self, month=cur_month, year=cur_year, excel=False):
        """
        Gets call/put data for the stock with the expiration data in the
        given month and year

        Parameters
        ----------
        month: number, int
            The month of the options expire.

        year: number, int
            The year the options expire.

        excel: bool, optional(default=False)
            A boolean value indicating whether or not the data should be saved
            to an excel spreadsheet. If true the name of the file will be
            "'ticker'_options.xlsx" unless otherwise indicated. Also there will
            be two sheets created. The first one is named 'calls' and contains
            the call data and the second is for the puts.

        Returns
        -------
        call_data: pandas.DataFrame
            A DataFrame with call options data.

        put_data: pandas.DataFrame
            A DataFrame with call options data.
        """

        mon_in = month if len(str(month)) == 2 else str('0' + str(month))

        url = str('http://finance.yahoo.com/q/op?s=' + self.symbol + '&m=' +
                  str(year) + '-' + str(mon_in))

        buf = urlopen(url)
        soup = BeautifulSoup(buf)
        body = soup.body

        tables = body.findAll('table')
        calls = tables[9]

        call_data = _parse_options_data(calls)

        if excel == True:
            file_name = str(str(self.symbol).upper() + '_calls.xlsx')
            writer = ExcelWriter(file_name)
            call_data.to_excel(writer, sheet_name='calls')
            writer.save()

        return call_data

    def get_put_data(self, month=cur_month, year=cur_year, excel=False):
        """
        Gets put data for the stock with the expiration data in the
        given month and year

        Parameters
        ----------
        month: number, int
            The month of the options expire.

        year: number, int
            The year the options expire.

        excel: bool, optional(default=False)
            A boolean value indicating whether or not the data should be saved
            to an excel spreadsheet. If true the name of the file will be
            "'ticker'_options.xlsx" unless otherwise indicated. Also there will
            be two sheets created. The first one is named 'calls' and contains
            the call data and the second is for the puts.

        Returns
        -------
        put_data: pandas.DataFrame
            A DataFrame with call options data.
        """

        mon_in = month if len(str(month)) == 2 else str('0' + str(month))

        url = str('http://finance.yahoo.com/q/op?s=' + self.symbol + '&m=' +
                  str(year) + '-' + str(mon_in))

        buf = urlopen(url)
        soup = BeautifulSoup(buf)
        body = soup.body

        tables = body.findAll('table')
        puts = tables[13]

        put_data = _parse_options_data(puts)

        if excel == True:
            file_name = str(str(self.symbol).upper() + '_puts.xlsx')
            writer = ExcelWriter(file_name)
            put_data.to_excel(writer, sheet_name='puts')
            writer.save()

        return put_data

    def get_near_stock_price(self, opt_df, above_below=2):
        """
        Cuts the data frame opt_df that is passed in to only take
        options that are near the current stock price.

        Parameters
        ----------
        opt_df: DataFrame
            The DataFrame that will be passed in to be cut down.

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
        price = get_quote_yahoo(['aapl'])['last']
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
            all_calls = pd.DataFrame()
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
                        all_calls = pd.concat([all_calls, call_frame])
                except:
                    pass

        if put:
            all_puts = pd.DataFrame()
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
                        all_puts = pd.concat([all_puts, put_frame])
                except:
                    pass

        if call and put:
            return [all_calls, all_puts]
        else:
            if call:
                return all_calls
            else:
                return all_puts


if __name__ == '__main__':
    aapl = Options('aapl')
    calls = aapl.get_call_data()
    puts = aapl.get_put_data()
    chopper = aapl.get_near_stock_price(calls)