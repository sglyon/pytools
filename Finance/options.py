from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
from pandas.io.parsers import TextParser, ExcelWriter


class Options():
	"""
	This class fetches call/put data for a given stock/expiration month.

	It is instantiated with a string representing the ticker symbol.

	The class has the following methods:
		get_options_data:(stock, month, year)
	"""

	def __init__(self, symbol):
		""" Instantiates options_data with a ticker saved as symbol """
		self.stock = str(symbol).upper()


	def get_options_data(self, month, year, excel=False):
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
		def _unpack(row, kind='td'):
			return [val.text for val in row.findAll(kind)]


		def parse_options_data(table):
			rows = table.findAll('tr')
			header = _unpack(rows[0], kind='th')
			data = [_unpack(r) for r in rows[1:]]
			return TextParser(data, names=header).get_chunk()

		mon_in = month if len(str(month)) == 2 else str('0' + str(month))

		url = str('http://finance.yahoo.com/q/op?s=' + self.stock + '&m=' +
				  str(year) + '-' + str(mon_in))

		buf = urlopen(url)
		soup = BeautifulSoup(buf)
		body = soup.body

		tables = body.findAll('table')
		calls = tables[9]
		puts = tables[13]

		rows = calls.findAll('tr')

		call_data = parse_options_data(calls)
		put_data = parse_options_data(puts)

		if excel==True:
			file_name = str(str(stock).upper() + '_options.xlsx')
			writer = ExcelWriter(file_name)
			put_data.to_excel(writer, sheet_name='puts')
			call_data.to_excel(writer, sheet_name='calls')
			writer.save()


		return [call_data, put_data]