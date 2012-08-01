import numpy as np
import pandas as pd
from pandas.io.parsers import TextParser, ExcelWriter
from yahooStocks import StockInfo
from dateutil import parser
from options import Options
import datetime as dt
from time import time


start_time = time()

nyse = pd.read_csv('NYSE_all_tickers.csv')

industries = list(nyse['industry'])
sectors = list(nyse['Sector'])
tickers = list(nyse['Symbol'])
names = list(nyse['Name'])
market_caps = list(nyse['MarketCap'])

tickers.sort()
num_tickers = len(tickers)

current_month = dt.datetime.now().month
current_day = dt.datetime.now().date
current_year = dt.datetime.now().year

# Generate instances of StockInfo class to get price, dividend yield, div/share,
#   and ex dividend date

# Also generate Options objects for the call data.

stocks = [StockInfo(tick) for tick in tickers]
options = [Options(tick) for tick in tickers]


ex_divs = []
ex_div_months = []
ex_div_days = []
prices = []
div_yield = []
div_per_share = []

for i in range(num_tickers):
    try:
        ex_divs.append(stocks[i].get_ex_dividend())
        ex_div_months.append(parser.parse(ex_divs[i]).month)
        ex_div_days.append(parser.parse(ex_divs[i]).day)
    except:
        ex_div_months.append('None')
        ex_div_days.append('None')
    prices.append(stocks[i].get_price())
    div_per_share.append(stocks[i].get_dividend_per_share())


# Build input month/year for option prices.
op_months = range(current_month + 1, current_month + 7)
abs_op_months = range(current_month + 1, current_month + 7)
op_years = [current_year] * 6

to_change = 0
for i in range(len(op_months)):
    if op_months[i] > 12:
        op_months[i] -= 12
        to_change += 1

for i in range(1, to_change + 1):
    op_years[-i] += 1

prices = np.asarray(prices)



final_frame = pd.DataFrame()

first_except = 0
second_except = 0
third_except = 0
fourth_except = 0

for ticker in range(num_tickers):
    if ex_divs[ticker] == 'N/A':
        for month in range(0,6):
            try:
                call_frame = options[ticker].get_options_data(op_months[month], op_years[month])[0]
                start_index = np.where(call_frame['Strike'] > prices[ticker])[0][0]


                temp_frame = pd.DataFrame()

                # Appending to the frame if possible.
                get_range = range(start_index - 2, start_index + 3)
                new_row = call_frame.ix[get_range,:3]
                temp_frame = temp_frame.join(new_row, how='right')

                # Now we have all the data we need for ticker, month, and year
                temp_frame2 = pd.DataFrame(temp_frame, columns=['Name',
                                                                'Symbol',
                                                                'Industry',
                                                                'Sector',
                                                                'Market Cap',
                                                                'Strike',
                                                                'Last',
                                                                'Exp. Date',
                                                                'Option Volume',
                                                                'Stock Price',
                                                                'Ex. Div Date',
                                                                'Num Divs.',
                                                                'Div/share',
                                                                'Div Inc',
                                                                'Gain/Loss Exercise',
                                                                'Total Income',
                                                                'Return',
                                                                'Annual Return'])

                temp_frame2.columns =['Name',
                                      'Ticker',
                                      'Industry',
                                      'Sector',
                                      'Market Cap',
                                      'Strike',
                                      'Option Price',
                                      'Exp. Date',
                                      'Option Volume',
                                      'Stock Price',
                                      'Ex. Div Date',
                                      'Num Divs.',
                                      'Div/share',
                                      'Div Inc',
                                      'Gain/Loss Exercise',
                                      'Total Income',
                                      'Return',
                                      'Annual Return']

                temp_frame2['Name'] = names[ticker]
                temp_frame2['Industry'] = industries[ticker]
                temp_frame2['Sector'] = sectors[ticker]
                temp_frame2['Market Cap'] = market_caps[ticker]
                temp_frame2['Option Volume'] = call_frame.ix[get_range, 6]
                temp_frame2['Ticker'] = tickers[ticker]
                temp_frame2['Exp. Date'] = str(str(op_months[month]) +
                                               ' - ' +str(op_years[month]))


                temp_frame2['Stock Price'] = prices[ticker]
                temp_frame2['Div/share'] = 'None'
                temp_frame2['Ex. Div Date'] = 'None'
                temp_frame2['Div Inc'] = 'None'
                temp_frame2['Num Divs.'] = 'None'

                temp_frame2['Gain/Loss Exercise'] = temp_frame2['Strike'] - \
                                                    temp_frame2['Stock Price']

                # Don't include gain from stock price movement.
                losses = temp_frame2['Gain/Loss Exercise'] < 0.0
                only_losses = temp_frame2['Gain/Loss Exercise'] * losses
                temp_frame2['Total Income'] = only_losses + \
                                              temp_frame2['Option Price']

                temp_frame2['Return'] = temp_frame2['Total Income'] / \
                                        temp_frame2['Stock Price']

                time_to_expiration = abs_op_months[month] - current_month
                temp_frame2['Annual Return'] = temp_frame2['Return'] * \
                                               (12. /  time_to_expiration)

                temp_frame2 = temp_frame2.dropna()

                if month == 0:
                    final_frame = final_frame.join(temp_frame2, how = 'right')
                else:
                    final_frame = pd.concat([final_frame, temp_frame2])


            except:
                pass

    else:
        for month in range(0,6):
            try:
                call_frame = options[ticker].get_options_data(op_months[month], op_years[month])[0]
                start_index = np.where(call_frame['Strike'] > prices[ticker])[0][0]


                temp_frame = pd.DataFrame()

                # Appending to the frame if possible.
                get_range = range(start_index - 2, start_index + 3)
                new_row = call_frame.ix[get_range,:3]
                temp_frame = temp_frame.join(new_row, how='right')

                # Now we have all the data we need for ticker, month, and year
                temp_frame2 = pd.DataFrame(temp_frame, columns=['Name',
                                                                'Symbol',
                                                                'Industry',
                                                                'Sector',
                                                                'Market Cap',
                                                                'Strike',
                                                                'Last',
                                                                'Exp. Date',
                                                                'Option Volume',
                                                                'Stock Price',
                                                                'Ex. Div Date',
                                                                'Num Divs.',
                                                                'Div/share',
                                                                'Div Inc',
                                                                'Gain/Loss Exercise',
                                                                'Total Income',
                                                                'Return',
                                                                'Annual Return'])

                temp_frame2.columns =['Name',
                                      'Ticker',
                                      'Industry',
                                      'Sector',
                                      'Market Cap',
                                      'Strike',
                                      'Option Price',
                                      'Exp. Date',
                                      'Option Volume',
                                      'Stock Price',
                                      'Ex. Div Date',
                                      'Num Divs.',
                                      'Div/share',
                                      'Div Inc',
                                      'Gain/Loss Exercise',
                                      'Total Income',
                                      'Return',
                                      'Annual Return']

                temp_frame2['Name'] = names[ticker]
                temp_frame2['Industry'] = industries[ticker]
                temp_frame2['Sector'] = sectors[ticker]
                temp_frame2['Market Cap'] = market_caps[ticker]
                temp_frame2['Option Volume'] = call_frame.ix[get_range, 6]
                temp_frame2['Ticker'] = tickers[ticker]
                temp_frame2['Exp. Date'] = str(str(op_months[month]) +
                                               ' - ' +str(op_years[month]))


                temp_frame2['Stock Price'] = prices[ticker]
                temp_frame2['Div/share'] = float(div_per_share[ticker]) / 100.
                temp_frame2['Ex. Div Date'] = str(str(ex_div_months[ticker]) +
                                                   ' - ' + str(ex_div_days[ticker]))

                # Figure out number of dividends.
                next_ex_div_month = ex_div_months[ticker] + 3
                two_next_ex_div_months = ex_div_months[ticker] + 6


                if current_month > ex_div_months[ticker]:
                    if abs_op_months[month] < next_ex_div_month:
                        temp_frame2['Num Divs.'] = 0.

                    elif abs_op_months[month] >= next_ex_div_month:
                        if abs_op_months[month] >= two_next_ex_div_months:
                            temp_frame2['Num Divs.'] = 2.
                        else:
                            temp_frame2['Num Divs.'] = 1.

                elif current_month < ex_div_months[ticker]:
                    if abs_op_months[month] < next_ex_div_month:
                        temp_frame2['Num Divs.'] = 1.

                    elif abs_op_months[month] >= next_ex_div_month:
                        if abs_op_months[month] >= two_next_ex_div_months:
                            temp_frame2['Num Divs.'] = 3.
                        else:
                            temp_frame2['Num Divs.'] = 2.

                elif current_month == ex_div_months[ticker]:
                    if current_day <= ex_div_days[ticker]:
                        if abs_op_months[month] < next_ex_div_month:
                            temp_frame2['Num Divs.'] = 1.

                        elif abs_op_months[month] >= next_ex_div_month:
                            if abs_op_months[month] >= two_next_ex_div_months:
                                temp_frame2['Num Divs.'] = 3.
                            else:
                                temp_frame2['Num Divs.'] = 2.

                    elif current_day > ex_div_days[ticker]:
                        if abs_op_months[month] < next_ex_div_month:
                            temp_frame2['Num Divs.'] = 0

                        elif abs_op_months[month] >= next_ex_div_month:
                            if abs_op_months[month] >= two_next_ex_div_months:
                                temp_frame2['Num Divs.'] = 2.
                            else:
                                temp_frame2['Num Divs.'] = 1.


                temp_frame2['Div Inc'] = temp_frame2['Num Divs.'] * \
                                         temp_frame2['Div/share']

                temp_frame2['Gain/Loss Exercise'] = temp_frame2['Strike'] - \
                                                    temp_frame2['Stock Price']

                # Don't include gain from stock price movement.
                losses = temp_frame2['Gain/Loss Exercise'] < 0.0
                only_losses = temp_frame2['Gain/Loss Exercise'] * losses
                temp_frame2['Total Income'] = only_losses + \
                                              temp_frame2['Div Inc'] +  \
                                              temp_frame2['Option Price']

                #temp_frame2['Total Income'] = temp_frame2['Gain/Loss Exercise'] + \
                #                              temp_frame2['Div Inc'] +  \
                #                              temp_frame2['Price']

                temp_frame2['Return'] = temp_frame2['Total Income'] / \
                                        temp_frame2['Stock Price']

                time_to_expiration = abs_op_months[month] - current_month
                temp_frame2['Annual Return'] = temp_frame2['Return'] * \
                                               (12. /  time_to_expiration)

                temp_frame2 = temp_frame2.dropna()

                if month == 0:
                    final_frame = final_frame.join(temp_frame2, how = 'right')
                else:
                    final_frame = pd.concat([final_frame, temp_frame2])


            except:
                pass

    print 'Just finished ticker %s of %s' % (ticker, num_tickers)


file_name = 'NYSE_covered_call.xlsx'
writer = ExcelWriter(file_name)
final_frame.to_excel(writer, sheet_name='Covered Call')
writer.save()

end_time = time()
elapsed_time = end_time - start_time
print elapsed_time
