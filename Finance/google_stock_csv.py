import urllib
from datetime import datetime
from threading import Thread
from Queue import Queue

base_url="http://ichart.finance.yahoo.com/table.csv?"

def get_historical(symbols,start=None,end=None,threads=0):
    if isinstance(symbols,str):
        return get_historical_single(symbols,start,end)
    quotes={}
    if threads:
        def quoter(): 
            while True: 
                data = q.get()
                quotes[data[0]]=get_historical_single(data[0],data[1],data[2])
                q.task_done()
        q = Queue() 
        for i in range(threads): 
             t = Thread(target=quoter)
             t.setDaemon(True)
             t.start() 
        for sym in symbols: q.put((sym,start,end))
        q.join()
    else:
        for sym in symbols:
            quotes[sym]=get_historical_single(sym,start,end)
    return quotes

def get_historical_single(symbol,start=None,end=None):
    full_url=base_url+"&s="+symbol
    if start:
        full_url+="&a=%i&b=%i&c=%i"%(start.month-1,start.day,start.year)
    if end:
        full_url+="&d=%i&e=%i&f=%i"%(end.month-1,end.day,end.year)
    full_url+="&g=d"
    quotes={}
    quotes['raw']=[]
    quotes['by_date']={}
    quotes['dates']=[]
    quotes['opens']=[]
    quotes['highs']=[]
    quotes['lows']=[]
    quotes['closes']=[]
    quotes['volumes']=[]
    quotes['adjusted_closes']=[]
    quotes_lines=urllib.urlopen(actual_url).read().split('\n')[1:-1]
    for quote_line in quotes_lines:
        #quote_line structure: Date,Open,High,Low,Close,Volume,Adj Close
        splt_q=quote_line.split(',')
        date=datetime(*(map(int,splt_q[0].split('-'))))
        op=float(splt_q[1])
        hi=float(splt_q[2])
        lo=float(splt_q[3])
        close=float(splt_q[4])
        vol=int(splt_q[5])
        adj_close=float(splt_q[6])
        quote=dict(date=date,open=op,high=hi,low=lo,close=close,volume=vol,adj_close=adj_close)
        quotes['raw'].append(quote)
        quotes['by_date'][date]=quote
        quotes['dates'].append(date)
        quotes['opens'].append(op)
        quotes['highs'].append(hi)
        quotes['lows'].append(lo)
        quotes['closes'].append(close)
        quotes['volumes'].append(volume)
        quotes['adjusted_closes'].append(adj_close)
    return quotes

if __name__ == '__main__':
    start_date=datetime(2005,1,1)
    symbols=['F.MI','AAPL','IBM','GOOG']
    quotes=get_historical(symbols,start_date=start_date,threads=4)
    for k in symbols:
        print '%s: %i quotes'%(k,len(quotes[k]['closes']))