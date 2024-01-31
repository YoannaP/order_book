import random
import logging
from datetime import datetime
from itertools import count

from classes.messages import *

class Trader:
    """
    Player in market who can create orders, cancel orders, receive
    aknowledgements from exchange and update its live orders based on exchange
    fills.
    """
    _N = count(1)
    def __init__(self):
        self.id = 'trader' + str(next(self._N))
        self.live_orders = []

    def __repr__(self):
        return self.id

    def sendOrderAdd(self, side, price, qty):
        """
        Sends a random add or cancel order to the exchange.

        Parameters
        ----------
        side (int): 1 for buy, -1 for sell
        price (float): +/- 10 from close price of 50.32, incremented by 0.01
        qty (int): quantity of trade ranges from 0-200.

        Returns
        -------
        orderAdd (OrderAdd object)

        """
        orderAdd = OrderAdd(traderID=self.id, side=side,
                                price=price, qty=qty)
        orderAdd.log_order_add()
        return orderAdd

    def sendOrderCancel(self, ord, qty):
        """
        Creates a random cancel order from trader's live orders.

        Parameters
        ----------
        ord (OrderAknowledgement object): Randomly chosen order from
            trader.live_orders to cancel or decrease
        qty (int): The quantity to cancel in the order. Rnadomly chosen by
            trader from 1 to maximum quantity of ord.

        Returns
        -------
        ordCancel (OrderCancel object)
        """
        ordCancel = OrderCancel(ord, qty)

        return ordCancel

    def receiveAknowledgement(self, orderAknowledgement):
        """
        Adds order aknowledgement from exchange to live trader orders.

        Parameters
        ----------
        orderAknowledgement (OrderAknowledgement object): this is made by
            exchange and passed to the trader
        """
        self.live_orders.append(orderAknowledgement)

    def updateLiveOrders(self):
        """
        When a fill is done at exchange, order quantity decreases to 0.
        Orders with 0 quantity are removed from live orders as they are filled
        or cancelled by trader.
        """
        self.live_orders = [i for i in self.live_orders if i.qty!=0]




if __name__ == "__main__":
    livetrader = Trader()
    livetrader2 = Trader()
    add_order = OrderAdd(livetrader.id)
