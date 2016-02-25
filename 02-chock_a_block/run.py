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
import sys

from stockfighter import Stockfighter
from stockfighter import GM

from docopt import docopt

import pandas as pd

pd.options.display.expand_frame_repr = False

argopts = docopt(__doc__)
qtyrequired = int(argopts['--qty'])
loopsize = int(argopts['--loop-size'])
previousnbfilled = 0

################################################
# Functions
################################################
def getGameState():
    while True:
        time.sleep(pause)
        state = gm.check(instanceid)
        if 'flash' not in state:
            continue

        return state['flash']['info']

def waitTargetPrice():
    while True:
        info = getGameState()
        m = re.match(r'.*target price is \$([0-9]+)\.([0-9]+).*', info)
        if m:
            targetprice = int("%s%s" % (m.group(1),m.group(2)))
            return targetprice


def waitAllordered():
    while True:

        # Check if orders is opened
        time.sleep(pause)
        stockinfo = s.status_for_all_orders_in_a_stock(stock)
        orders = stockinfo['orders']

        opened = False
        for order in orders:
            opened = opened or order['open']

        if not opened:
            break

    # Compute all orders
    totalnbfilled = 0
    totalsumprice = 0
    for order in orders:
        for fill in order['fills']:
            totalnbfilled += int(fill['qty'])
            totalsumprice += (int(fill['qty']) * int(fill['price']))

    return {
        'totalnbfilled': totalnbfilled,
        'totalsumprice': totalsumprice,
        'totalavgprice': int(totalsumprice / totalnbfilled)
    }

################################################
# Game init
################################################

# Get game informations
print ("Init game")
gm = GM()
varsgame = gm.start('chock_a_block')
instanceid = varsgame['instanceId']

# Restart game
print ("Restart game")
varsgame = gm.restart(instanceid)
instanceid = varsgame['instanceId']
state = gm.check(instanceid)
# Check if the game is initialized
while 'details' not in state:
    time.sleep(1)
    state = gm.check(instanceid)

account = varsgame['account']
venue = varsgame['venues'][0]
stock = varsgame['tickers'][0]
pause = 1 # varsgame['secondsPerTradingDay']

print ("Init stockfighter")
s = Stockfighter(venue=venue, account=account)

################################################
# Search target price
################################################

# Execute one bid for searching target client price
print ("Search client target price")
s.place_new_order(stock, 1, 1, 'buy', 'market')

# Extract target price
targetprice = waitTargetPrice()
print ('The target client price is %(targetprice)s' % locals())
requiredtotalprice = targetprice * qtyrequired
qtyrequiredprice = targetprice * qtyrequired

################################################
# Buy in immediate-or-cancel mode
################################################

while True:
    orderinfo = waitAllordered()
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
    order = s.place_new_order(stock, newtargetprice, nextnbfill, 'buy', 'immediate-or-cancel')
    state = gm.check(instanceid)

    if 'info' not in state['flash']:
        break

    flashinfo = state['flash']['info']

################################################
# Show results
################################################

print ("")
stockinfo = s.status_for_all_orders_in_a_stock(stock)
orders = stockinfo['orders']

stockprices = []
for order in orders:
    for fill in order['fills']:
        stockprices.append(fill)

df_allstocks = pd.DataFrame(stockprices)
df_uniqstocks = df_allstocks.drop_duplicates()
print(df_uniqstocks)