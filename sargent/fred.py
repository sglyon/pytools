"""
Created Feb 4, 2013

Author: Spencer Lyon and Chase Coleman

Pure python module for getting data from FRED
"""
import urllib2
import datetime as dt
import csv


def _parse_dates(date):
    """
    Parses the string or tuple passed in as the date argument and
    converts it into a standard datetime object.

    Parameters
    ----------
    date: tuple, str
        A tuple or string giving the date and time in month, day, year
        format. For example, the tuple and string for December 31, 2012
        would be (12, 31, 2012) and '12/31/2012', respectively.

    Returns
    -------
    dt_date: dt.datetime()
        A date time object representing the date passed in
    """
    if type(date) == tuple:
        if len(str(date[-1])) != 4:
            raise ValueError('Date in incorrect format. Read docstring \
                             and try again')
        else:
            month = date[0]
            day = date[1]
            year = date[2]
            dt_date = dt.datetime(year, month, day)

    elif type(date) == str:
        if date[-4:-2] != '20' and date[-4:-2] != '19':
            raise ValueError('Date in incorrect format. Read docstring \
                             and try again')
        else:
            mon_s, day_s, yr_s = date.split('/')
            year = int(yr_s)
            month = int(mon_s)
            day = int(day_s)
            dt_date = dt.datetime(year, month, day)

    else:
        raise ValueError('date parameter must be a string or tuple')

    return dt_date


def fred_data(name, start=(1, 1, 2010), end=dt.datetime.today()):
    """
    Download data from FRED and return a list of dates and a list of
    values.

    Parameters
    ----------
    name: str
        A string representing the object you would like to download from
        FRED.

    start: tuple or str, optional(default=(1, 1, 2010))
        The starting date for which you would like the data. This must
        be a tuple or a string in month, day, year format. For example,
        the tuple and string for December 31, 2012 would be
        (12, 31, 2012) and '12/31/2012', respectively.

    end: tuple or str, optional(default=dt.datetime.today())
        The ending date for which you would like the data. This must
        be a tuple or a string in month, day, year format. For example,
        the tuple and string for December 31, 2012 would be
        (12, 31, 2012) and '12/31/2012', respectively.

    Returns
    -------
    dates: list
        A list of dates associated with the data

    data: list
        A list of the requested data
    """
    # Clean dates
    start = _parse_dates(start)
    end = end if type(end) == dt.datetime else _parse_dates(end)

    # Create url for data
    fred_URL = "http://research.stlouisfed.org/fred2/series/"

    url = fred_URL + '%s' % name + '/downloaddata/%s' % name + '.csv'

    raw = list(csv.reader(urllib2.urlopen(url)))  # Get data

    # pull out dates and data
    raw_dates = [raw[i][0] for i in range(1, len(raw))]
    raw_data = [raw[i][1] for i in range(1, len(raw))]

    # convert dates to datetime objects
    all_dates = []
    for i in raw_dates:
        pieces = i.split('-')
        yr = int(pieces[0])
        mon = int(pieces[1])
        day = int(pieces[2])
        all_dates.append(dt.datetime(yr, mon, day))

    # pull out only data between start and end dates
    data = []
    dates = []
    for i in range(len(all_dates)):
        if all_dates[i] >= start and all_dates[i] <= end:
            data.append(raw_data[i])
            dates.append(all_dates[i])

    return data, dates


def prep_for_google(name, start=(1, 1, 2010), end=dt.datetime.today(),
                    filename='test.txt'):
    """
    Generates a file with javascript code used to create a DataTable
    object to be used in the google Chart API. The format of the code
    follows the example from the follwing url:

        http://code.google.com/apis/ajax/playground/
                ?type=visualization#annotated_time_line

    Parameters
    ----------
    name: str
        A string representing the object you would like to download from
        FRED.

    start: tuple or str, optional(default=(1, 1, 2010))
        The starting date for which you would like the data. This must
        be a tuple or a string in month, day, year format. For example,
        the tuple and string for December 31, 2012 would be
        (12, 31, 2012) and '12/31/2012', respectively.

    end: tuple or str, optional(default=dt.datetime.today())
        The ending date for which you would like the data. This must
        be a tuple or a string in month, day, year format. For example,
        the tuple and string for December 31, 2012 would be
        (12, 31, 2012) and '12/31/2012', respectively.

    filename: str, optional(default='test.txt')
        A string specifying the file name for the created javascript
        code. If none is given,

    Returns
    -------
    None:
        This function simply creates a new file in the current
        directory called filename

    Notes
    -----
    This function calls fred_data to generate the data.
    """
    # Get the data
    data, dates = fred_data(name, start, end)
    # First lines, initialize the data JSON object and add columns
    lines = "function drawVisualization() {\n"
    lines += "var data = new google.visualization.DataTable();\n"
    lines += "data.addColumn('date', 'Date');\n"
    lines += "data.addColumn('number', '%s');\n" % (name)
    # lines += "data.addColumn('string', 'title1');\n"
    # lines += "data.addColumn('string', 'text1');\n"
    lines += "data.addRows([\n"

    rows = ""

    for i in range(len(data)):
        t_date = dates[i]  # Get this date
        yr = t_date.year
        mon = t_date.month
        day = t_date.day
        if i != len(data) - 1:
            rows += "  [new Date(%i, %i, %i), %.3f],\n" % (yr, mon, day,
                                                          float(data[i]))
        else:
            rows += "  [new Date(%i, %i, %i), %.3f]\n" % (yr, mon, day,
                                                          float(data[i]))

    l5 = ']);\n\n'

    end_lines = "var annotatedtimeline = new \
                google.visualization.AnnotatedTimeLine(\n"
    end_lines += "    document.getElementById('visualization'));\n"
    end_lines += "annotatedtimeline.draw(data, {'displayAnnotations': \
                                                            true});\n}"

    f = open(filename, 'w')
    f.write(lines)
    f.write(rows)
    f.write(l5)
    f.write(end_lines)
    f.close()

if __name__ == '__main__':
    # Run test case.
    name = 'CPIAUCSL'  # CPI index of all urban consumers: all items
    starter = '4/3/1999'  # Start date
    ender = '2/1/2005'  # End date
    data, dates = fred_data(name, starter, ender)  # Get the data
    prep_for_google(name, starter, ender)
