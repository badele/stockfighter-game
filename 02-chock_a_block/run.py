#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage:
  level1 [-q=<qorder> | --qty=<qorder>] [-l=<nb> | --loop-size=<nb>]
  level1 -h | --help

Arguments:

Options:
  -l=<nb> --loop-size=<nb>          Loop number [default: 10000]
  -q=<qorder> --qty=<qorder>        Stock quantity must be order [default: 100000]
  -h --help                         Help usage

"""

__authors__ = 'Bruno Adelé <bruno@adele.im>'
__copyright__ = 'Copyright (C) 2016 Bruno Adelé'
__description__ = """Stockfighter python game solutions"""
__license__ = 'GPL'
__commitnumber__ = "$id$"

import re
import time

from stockfighter import Stockfighter
from stockfighter import GM

from docopt import docopt

import pandas as pd

import commons as lib


pd.options.display.expand_frame_repr = False

argopts = docopt(__doc__)
qtyrequired = int(argopts['--qty'])
loopsize = int(argopts['--loop-size'])
previousnbfilled = 0

################################################
# Functions
################################################
def waitTargetPrice():
    while True:
        info = sgame.getGameState()
        m = re.match(r'.*target price is \$([0-9]+)\.([0-9]+).*', info)
        if m:
            targetprice = int("%s%s" % (m.group(1),m.group(2)))
            return targetprice


# Init game
sgame = lib.SGame('chock_a_block', True)

# Execute one bid for searching target client price
print ("Search client target price")
sgame.sf.place_new_order(sgame.stock, 1, 1, 'buy', 'market')

# Extract target price
targetprice = waitTargetPrice()
print ('The target client price is %(targetprice)s' % locals())
requiredtotalprice = targetprice * qtyrequired
qtyrequiredprice = targetprice * qtyrequired

################################################
# Buy in immediate-or-cancel mode
################################################

while True:
    orderinfo = sgame.waitAllordered()
    previousnbfilled = orderinfo['totalnbfilled']
    previoussumprice = orderinfo['totalsumprice']

    if previousnbfilled >= qtyrequired:
        break

    # Compute new price
    remainingnbfill = qtyrequired - previousnbfilled
    nextnbfill = min(remainingnbfill, loopsize)
    nextfilloffset = previousnbfilled + nextnbfill

    nextsumprice = nextfilloffset * targetprice
    newtargetprice = int((nextsumprice - previoussumprice) / nextnbfill)

    print ('.',end = "", flush=True)
    order = sgame.sf.place_new_order(sgame.stock, newtargetprice, nextnbfill, 'buy', 'immediate-or-cancel')
    flashinfo = sgame.getGameState()

################################################
# Show results
################################################

print ("")
stockinfo = sgame.sf.status_for_all_orders_in_a_stock(sgame.stock)
orders = stockinfo['orders']

stockprices = []
for order in orders:
    for fill in order['fills']:
        stockprices.append(fill)

df_allstocks = pd.DataFrame(stockprices)
df_uniqstocks = df_allstocks.drop_duplicates()
print(df_uniqstocks)