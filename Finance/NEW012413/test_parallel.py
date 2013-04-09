"""
Created Mar 29, 2013

Author: Spencer Lyon

Test the parallel algorithm I wrote to speed up data retrieval
"""
from __future__ import division
import os
# from dateutil import parser
# import datetime as dt
# import urllib
# import urllib2
# import numpy as np
import pandas as pd
# from pandas.io.parsers import ExcelWriter
# from pandas.io.data import get_data_yahoo
# from options import Options, _parse_options_data
# from yahooStocks import StockInfo
# from lxml.html import parse
from mpi4py import MPI
from byumcl.partools.partools import gatv_scatv_tuples, rprint, par_print

comm = MPI.COMM_WORLD
rank = comm.Get_rank()  # Which process we are on
size = comm.Get_size()  # Total number of processes

pd.set_option('line_width', 200)

if rank == 0:
    nyse = pd.DataFrame.from_csv('nyse_tickers.csv')
    nas = pd.DataFrame.from_csv('nasdaq_tickers.csv')

    raw_big = pd.concat([nyse, nas])

    # Contains one line per ticker
    big = raw_big.sort_index()
else:
    big = None

# Share big
comm.Barrier()  # Have everyone wait for root to get things started
big = comm.bcast(big, 0)  # Send the root process's big to everyone
comm.Barrier()  # Pause here to make sure all processes big

# Split it up and do the work!
cts, disps = gatv_scatv_tuples(size, big.shape[0])
locs = list(disps)
locs.append(big.shape[0])

# par_print(comm, 'This is my big shape %s' % (str(big.shape)))

my_start = int(locs[rank])
my_end = int(locs[rank + 1])

my_chunk = big.ix[my_start:my_end]

# par_print(comm, 'These are my chunk stats %s' % (my_chunk.__str__()[38:69]))

my_save_name = '##chunk%s.dat##' % (rank)
my_chunk.save(my_save_name)

par_print(comm, "my save name %s" % (my_save_name))

comm.Barrier()  # Make sure root stops here to have all files saved

# Let the root process finish it off
if rank == 0:
    tempbig = pd.DataFrame()
    for i in range(size):
        temp_name = '##chunk%s.dat##' % (i)
        temp_chunk = pd.DataFrame.load(temp_name)
        tempbig = pd.concat([tempbig, temp_chunk])
        os.remove(temp_name)

    tempbig.save('tempbig.db')
    big.save('big.db')
