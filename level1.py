#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage:
  level1 [-q=<qorder> | --qty=<qorder>] [-n=<nb> | --nb-loop=<nb>]
  level1 -h | --help

Arguments:

Options:
  -n=<nb> --nb-loop=<nb>        Loop number [default: 4]
  -q=<qorder> --qty=<qorder>    Stock quantity must be order [default: 100]
  -h --help                     Help usage

"""

__authors__ = 'Bruno Adelé <bruno@adele.im>'
__copyright__ = 'Copyright (C) 2016 Bruno Adelé'
__description__ = """Stockfighter python game solutions"""
__license__ = 'GPL'
__commitnumber__ = "$id$"

import time

from docopt import docopt
from stockfighter import Stockfighter
from stockfighter import GM

argopts = docopt(__doc__)

# Get game informations
gm = GM()
varsgame = gm.start('first_steps')
account = varsgame['account']
venue = varsgame['venues'][0]
stock = varsgame['tickers'][0]
pause = varsgame['secondsPerTradingDay']

s = Stockfighter(venue=venue, account=account)

# Compute mini/maxi prices
bidprices = []
askprices = []
for i in range(0, int(argopts['--nb-loop'])):
    # Get stock informations
    stockavg = s.quote_for_stock(stock=stock)

    # Get stock prices
    if 'bid' in stockavg:
        bidprices.append(stockavg['bid'])
    if 'ask' in stockavg:
        askprices.append(stockavg['ask'])

    # Wait
    time.sleep(pause)

# Get mini/maxi price
bidmin = min(bidprices)

# New order
qty = int(argopts['--qty'])
print ("Buy %(qty)s stocks at %(bidmin)s" % locals())
print (s.place_new_order(stock, bidmin, qty, 'buy', 'limit'))
