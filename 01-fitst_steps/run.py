#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage:
  level1 [-q=<qorder> | --qty=<qorder>] [-a=<nb> | --analyze-loop=<nb>]
  level1 -h | --help

Arguments:

Options:
  -a=<nb> --analyze-loop=<nb>   Loop number [default: 10]
  -q=<qorder> --qty=<qorder>    Stock quantity must be order [default: 100]
  -h --help                     Help usage

"""

__authors__ = 'Bruno Adelé <bruno@adele.im>'
__copyright__ = 'Copyright (C) 2016 Bruno Adelé'
__description__ = """Stockfighter python game solutions"""
__license__ = 'GPL'
__commitnumber__ = "$id$"

import time

from stockfighter import Stockfighter
from stockfighter import GM

from docopt import docopt

import pandas as pd

pd.options.display.expand_frame_repr = False

argopts = docopt(__doc__)

# Get game informations
print ("Init game")
gm = GM()
varsgame = gm.start('first_steps')
account = varsgame['account']
venue = varsgame['venues'][0]
stock = varsgame['tickers'][0]
pause = 1 # varsgame['secondsPerTradingDay']

print ("Init stockfighter")
s = Stockfighter(venue=venue, account=account)

# Compute mini/maxi prices
stockprices = []
aloop = int(argopts['--analyze-loop'])
for i in range(0, aloop):
    # Get stock informations
    print ('.',end = "", flush=True)

    stockinfo = s.quote_for_stock(stock=stock)
    stockprices.append(stockinfo)

    time.sleep(pause)

# Print stocks result
print ('')
df_allstocks = pd.DataFrame(stockprices)
df_uniqstocks = df_allstocks.drop_duplicates()
df_binmin = df_uniqstocks.min()

print ("Stocks")
print (df_uniqstocks[['venue', 'symbol', 'quoteTime', 'bid', 'ask', 'bidSize', 'askSize', 'bidDepth', 'askDepth']])

# New order
bidmin = int(df_binmin['bid'])
qty = int(argopts['--qty'])
print ("Buy %(qty)s stocks at %(bidmin)s" % locals())
print (s.place_new_order(stock, bidmin, qty, 'buy', 'limit'))
