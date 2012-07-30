import urllib2
import cookielib
import re
import time
import pickle
import sys
import os
import shutil
from time import strftime

def downloadAllTickersFromYahoo():
    if os.path.exists('Status.pck'):
        file = open('Status.pck', "r")
        BeginningIteration = pickle.load(file)
        file.close()
    else:
        BeginningIteration = 0

    if os.path.exists('dictOfTickers.pck'):
        file = open("dictOfTickers.pck", "r")
        dictOfTickers = pickle.load(file)
        file.close()
    else:
        dictOfTickers = dict()

    p = re.compile('\\\([^\\<\/td\ *\>\([^\<]*)\<\/td\ *\>\[^\<]*\<\/td\ *\>\([^\<]*)\<\/td\ *\>\([^\<]*)\<\/td\ *\>\([^\<]*)\<\/td\ *\>\<\/tr\ *\>')
    p2 = re.compile('\\\([^\\<\/td\ *\>\([^\<]*)\<\/td\ *\>\[^\<]*\<\/td\ *\>\([^\<]*)\<\/td\ *\>\\([^\\<\/td\ *\>\([^\<]*)\<\/td\ *\>\<\/tr\ *\>')
    p3 = re.compile('\\\([^\\<\/td\ *\>\([^\<]*)\<\/td\ *\>\[^\<]*\<\/td\ *\>\([^\<]*)\<\/td\ *\>\\([^\\<\/td\ *\>\([^\<]*)\<\/td\ *\>\<\/tr\ *\>')
    p4 = re.compile('\\\([^\\<\/td\ *\>\([^\<]*)\<\/td\ *\>\[^\<]*\<\/td\ *\>\([^\<]*)\<\/td\ *\>\([^\<]*)\<\/td\ *\>\([^\<]*)\<\/td\ *\>\<\/tr\ *\>')
    nextPage = re.compile('\Next\<\/a\>')
    i = 0

    universe = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','-','.','^','0','1','2','3','4','5','6','7','8','9','']

    for l1 in range (0,len(universe)):
        for l2 in range (0,len(universe)):
            for l3 in range (0,len(universe)):
                for l4 in range (0,len(universe)):
                    if i >= BeginningIteration:
                        letter =universe[l1] + universe[l2] + universe[l3] + universe[l4]
                        url = 'http://finance.yahoo.com/lookup?s=%s' % letter

                        finished = False

                        cj = cookielib.CookieJar()
                        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                        opener.addheaders = [('User-agent', 'Mozilla/5.0')]

                        while not finished:

                            connected = False
                            while not connected:
                                try:
                                    website = opener.open(url).read()
                                    connected = True
                                except Exception, e:
                                    print e
                                    print "URL is " + url
                                    time.sleep(60)
                                    print "Resuming ..."

                            pageResults = p.findall(website)
                            pageResults.extend(p2.findall(website))
                            pageResults.extend(p3.findall(website))
                            pageResults.extend(p4.findall(website))

                            for record in pageResults:
                                if not dictOfTickers.has_key(record[0]):
                                    dictOfTickers[record[0]] = record

                            nextPageUrl = nextPage.findall(website)
                            if len(nextPageUrl) == 0:
                                finished = True
                            else:
                                url = 'http://finance.yahoo.com' + nextPageUrl[0]

                            print strftime("%Y%m%d %H%M%S") + " " + letter + " #" + str(i) + ": Number of downloaded tickers: " + str(len(dictOfTickers))

                            FileID = str( i % 2 )

                            file = open("dictOfTickers" + FileID +".tmp", "w")
                            pickle.dump(dictOfTickers, file)
                            file.close()

                            file = open("Status"+FileID + ".tmp", "w")
                            pickle.dump(i, file)
                            file.close()

                            shutil.copyfile("dictOfTickers" + FileID +".tmp", "dictOfTickers.pck")
                            shutil.copyfile("Status" + FileID +".tmp", "Status.pck")

                    i+=1
    return

while(True):
    downloadAllTickersFromYahoo()
    os.remove("*.tmp")
    os.remove("Status.pck")
