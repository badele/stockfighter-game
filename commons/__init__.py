#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from stockfighter import Stockfighter
from stockfighter import GM

class SGame(object):
    def __init__(self, levelname, restart=False):
        """Init game"""

        print ("Init game")
        self.gm = GM()
        gameinfo = self.gm.start(levelname)
        self.instanceid = gameinfo['instanceId']

        # Restart game
        if restart:
            print ("Restart game")
            gameinfo = self.gm.restart(self.instanceid)
            self.instanceid = gameinfo['instanceId']
            state = self.gm.check(self.instanceid)
            # Check if the game is initialized
            while 'details' not in state:
                print ('state')
                time.sleep(1)
                state = self.gm.check(self.instanceid)

        # Set games variables
        self.account = gameinfo['account']
        self.venue = gameinfo['venues'][0]
        self.stock = gameinfo['tickers'][0]
        self.pause = 1

        print("Init stockfighter")
        self.sf = Stockfighter(venue=self.venue, account=self.account)


    def getGameState(self):
        while True:
            time.sleep(self.pause)
            state = self.gm.check(self.instanceid)
            if 'flash' not in state:
                continue

            return state['flash']['info']


    def analyseQuotes(self, nbloop, trades=None):
        if not trades:
            trades = []

        for i in range(0, nbloop):
            # Get stock informations
            print ('.',end = "", flush=True)

            stockinfo = self.sf.quote_for_stock(stock=self.stock)
            trades.append(stockinfo)

            time.sleep(self.pause)

        return trades


    def waitAllordered(self):
        while True:

            # Check if orders is opened
            time.sleep(self.pause)
            stockinfo = self.sf.status_for_all_orders_in_a_stock(self.stock)
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

        # Compute avg price
        try:
            totalavgprice = int(totalsumprice / totalnbfilled)
        except ZeroDivisionError:
            totalavgprice = 0

        return {
            'totalnbfilled': totalnbfilled,
            'totalsumprice': totalsumprice,
            'totalavgprice': totalavgprice
        }

    def getBookOrders(self):
        # Check if orders is opened
        time.sleep(self.pause)
        stockinfo = self.sf.status_for_all_orders_in_a_stock(self.stock)
        orders = stockinfo['orders']

        # Store orders
        buylist = []
        selllist = []
        for order in orders:
            tolist = buylist if 'buy' in order['direction'] else selllist
            for fill in order['fills']:
                tolist.append(fill)

        if len(buylist) == 0:
            buylist = [{'qty': 0, 'price': 0}]

        if len(selllist) == 0:
            selllist = [{'qty': 0, 'price': 0}]

        return {'buy': buylist, 'sell': selllist}