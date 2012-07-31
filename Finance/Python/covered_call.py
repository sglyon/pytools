import numpy as np
import pandas as pd
from pandas.io.parsers import TextParser, ExcelWriter
from yahooStocks import StockInfo
from dateutil import parser
from options import Options
import datetime as dt
from time import time

start_time = time()

# Top 100 dividend yield stocks per
# http://seekingalpha.com/article/283872-the-top-100-dividend-stocks-august-2011
tickers = ['FTR', 'WIN', 'CTL', 'PBI', 'RAI', 'T', 'CINF', 'MO', 'POM', 'RRD',
           'VZ', 'HCN', 'TEG', 'DUK', 'AEE',  'HCP', 'LLY', 'PPL', 'AEP',
           'LEG', 'PBCT', 'ETR', 'PNW', 'SCG', 'FE', 'LO', 'SO' , 'EXC', 'DTE',
           'TE', 'BMY', 'NI', 'ED', 'FII', 'MRK', 'PCL', 'PCG', 'PAYX', 'CMS',
           'XEL', 'WM', 'KMB', 'PEG', 'PFE', 'MCHP', 'D', 'SVU', 'CNP', 'HRB',
           'NEE', 'LMT', 'HCBK', 'SE', 'RTN', 'SRE', 'KIM', 'INTC', 'ABT', 'NUE',
           'COP', 'HNZ', 'PM', 'NYX', 'CAG', 'IP', 'KLAC', 'JNJ', 'AVP',' CPB',
           'MAT', 'MOLX','PG', 'SYY', 'GAS', 'DPS','WEC', 'GPC', 'DRI', 'KFT',
           'EIX', 'GE', 'CLX', 'NOC', 'LLTC', 'GIS', 'MTB', 'NU', 'PEP', 'MWV',
           'DD', 'PSA', 'AVY', 'IRM', 'PLD', 'OKE', 'K',' BLK', 'BMS', 'HAS']

num_tickers = len(tickers)

current_month = dt.datetime.now().month
current_day = dt.datetime.now().date
current_year = dt.datetime.now().year


## TODO:
#    Get:
#        stock price
#        dividend yield
#        dividend per share
#        ex dividend date
#        option price (use avg. of bid/ask. If within 0.01 use bid)
#        option expiration date
#        strike price.
#    Build dad's table:
#        columns:
#            1. ticker
#            2. stock price
#            3. option price
#            4. option date
#            5. ex_dividend date
#            6. dividend per share
#            7. gain/loss from stock price movement
#            8. total income (option price + div/share + gain/loss)
#            9. return (total income / stock price)

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
caps = []  # Market cap

for i in range(num_tickers):
    ex_divs.append(stocks[i].get_ex_dividend())
    prices.append(stocks[i].get_price())
    div_yield.append(stocks[i].get_dividend_yield())
    div_per_share.append(stocks[i].get_dividend_per_share())
    ex_div_months.append(parser.parse(ex_divs[i]).month)
    ex_div_days.append(parser.parse(ex_divs[i]).day)
    caps.append(stocks[i].get_market_cap())

# Build input month/year for option prices.
op_months = range(current_month + 1, current_month + 7)
abs_op_months = range(current_month + 1, current_month + 7)
op_years = [current_year] * 6

to_change = 0
for i in range(len(op_months)):
    if op_months[i] > 12:
        op_months[i]-= 12
        to_change += 1

for i in range(1, to_change + 1):
    op_years[-i] += 1

prices = np.asarray(prices)



final_frame = pd.DataFrame()

for ticker in range(len(tickers)):


    # Test case for first ticker
    for month in range(0,6):
        try:
            call_frame = Options(tickers[ticker]).get_options_data(op_months[month], op_years[month])[0]
            start_index = np.where(call_frame['Strike'] > prices[0])[0][0]


            temp_frame = pd.DataFrame()

            # Appending to the frame if possible.
            try:
                get_range = range(start_index - 2, start_index + 3)
                new_row = call_frame.ix[get_range,:3]
                temp_frame = temp_frame.join(new_row, how='right')

            except:

                try:
                    get_range = range(start_index -1 , start_index + 2)
                    new_row = call_frame.ix[get_range, :3]
                    temp_frame = temp_frame.join(new_row, how='right')

                except:

                    try:
                        get_range = range(start_index, start_index +1)
                        new_row = call_frame.ix[get_range, :3]
                        temp_frame = temp_frame.join(new_row, how='right')

                    except:
                        try:
                            new_row = call_frame.ix[start_index, :3]
                            temp_frame = temp_frame.join(new_row, how='right')

                        except:
                            pass


            # Now I should have all the options data for the first month, year combo.
            temp_frame2 = pd.DataFrame(temp_frame, columns=['Strike',
                                                            'Symbol',
                                                            'Last',
                                                            'Exp. Date',
                                                            'Stock Price',
                                                            'Ex. Div Date',
                                                            'Num Divs.',
                                                            'Div/share',
                                                            'Div Inc',
                                                            'Gain/Loss Exercise',
                                                            'Total Income',
                                                            'Return',
                                                            'Annual Return'])

            temp_frame2.columns = ['Strike',
                                   'Ticker',
                                   'Price',
                                   'Exp. Date',
                                   'Stock Price',
                                   'Ex. Div Date',
                                   'Num Divs.',
                                   'Div/share',
                                   'Div Inc',
                                   'Gain/Loss Exercise',
                                   'Total Income',
                                   'Return',
                                   'Annual Return']

            temp_frame2['Ticker'] = tickers[ticker]
            temp_frame2['Exp. Date'] = str(str(op_months[month]) +
                                           ' - ' +str(op_years[month]))


            temp_frame2['Stock Price'] = prices[ticker]
            temp_frame2['Div/share'] = div_per_share[ticker] / 100.
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
                                          temp_frame2['Price']

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

    print 'Just finished ticker %.1f' % ticker


file_name = 'covered_call.xlsx'
writer = ExcelWriter(file_name)
final_frame.to_excel(writer, sheet_name='Covered Call')
writer.save()




# TODO: fix the number of dividends column in the data frame. all entries are 0 right now






end_time = time()
elapsed_time = end_time - start_time
print elapsed_time
