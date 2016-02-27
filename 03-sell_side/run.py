#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage:
  level1 [-s=<nbshare> | --nb-share=<nbshare>] [-p=<nbprofit> | --nb-profit=<nbprofit>] [-a=<nb> | --analyze-loop=<nb>]
  level1 -h | --help

Arguments:

Options:
  -s=<nbshare> --nb-share=<nbshare>     Max Nb Share [default: 100]
  -p=<nbprofit> --qty=<qorder>          Nb profit [default: 10000]
  -a=<nb> --analyze-loop=<nb>           Analyze loop number [default: 5]
  -h --help                             Help usage

"""

__authors__ = 'Bruno Adelé <bruno@adele.im>'
__copyright__ = 'Copyright (C) 2016 Bruno Adelé'
__description__ = """Stockfighter python game solutions"""
__license__ = 'GPL'
__commitnumber__ = "$id$"

import pandas as pd
from docopt import docopt

import commons as lib

# Init parameters
pd.options.display.expand_frame_repr = False
argopts = docopt(__doc__)
aloop = int(argopts['--analyze-loop'])
nbshare = int(argopts['--nb-share'])

# Init game
sgame = lib.SGame('sell_side', True)

# Analyse last orders
while True:
    stockprices = sgame.analyseQuotes(aloop)
    df_allstocks = pd.DataFrame(stockprices)
    df_uniqstocks = df_allstocks.drop_duplicates()

    # Not more orders for compute
    # Get min/max value
    try:
        df_binmin = int(df_uniqstocks['bid'].min() * 1.02)
        df_binmax = int(df_uniqstocks['ask'].max() * 0.98)
    except:
        continue

    # Get previous orders
    ordersinfo = sgame.getBookOrders()

    # Buy informations
    df_stocksbuy = pd.DataFrame(ordersinfo['buy'])
    df_uniquebuy = df_stocksbuy.drop_duplicates()
    rawtotalprice = df_uniquebuy['qty'] * df_uniquebuy['price']
    df_uniquebuy['total'] = rawtotalprice
    buysumprice = int(df_uniquebuy['total'].sum())
    buysumqty = int(df_uniquebuy['qty'].sum())
    buyavgprice = int(buysumprice / buysumqty) if buysumqty > 0 else 0

    # Sell informations
    df_stocksell = pd.DataFrame(ordersinfo['sell'])
    df_uniquesell = df_stocksell.drop_duplicates()
    rawtotalprice = df_uniquesell['qty'] * df_uniquesell['price']
    df_uniquesell['total'] = rawtotalprice
    sellsumprice = int(df_uniquesell['total'].sum())
    sellsumqty = int(df_uniquesell['qty'].sum())
    sellavgprice = sellsumprice / sellsumqty if sellsumqty > 0 else 0

    delta = int(df_uniquesell['qty'].sum() - df_uniquebuy['qty'].sum())
    deltaavgprice = float(sellavgprice / buyavgprice) if buyavgprice>0 else 0

    previousnbfilled = int(df_uniquebuy['qty'].sum())
    previoussumprice = int(df_uniquebuy['total'].sum())
    previousavgprice = int(df_uniquebuy['total'].mean())

    if abs(delta) >= nbshare:
        continue

    if df_binmin >= df_binmax:
        continue

    tobuy = int(nbshare / 4)
    print ("Buy %(tobuy)s stocks at %(df_binmin)s" % locals())
    order = sgame.sf.place_new_order(sgame.stock, df_binmin, tobuy, 'buy', 'limit')
    if delta < 0:
        tosell = abs(delta)
        print("Sell %(tosell) stocks at %(df_binmax)s" % locals())
        order = sgame.sf.place_new_order(sgame.stock, df_binmax, tosell, 'sell', 'limit')

