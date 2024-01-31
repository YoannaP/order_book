from datetime import datetime
import logging
from itertools import count
import random


class OrderAdd:
    """
    Class to create a new order (with random parameters).
    -called by a trader.
    """
    def __init__(self, traderID, side, price, qty):
        """
        Parameters
        ----------
        traderID (str): of the format trader{N} where N is from 1-10
        side (int): 1 for buy, -1 for sell
        price (float): +/- 10 from close price of 50.32, incremented by 0.01
        qty (int): quantity of trade ranges from 0-200.
        """
        self.traderID = traderID
        self.side = side
        self.price = price
        self.qty = qty
        self.ts = datetime.now()


    def __repr__(self):
        return f"[orderAdd, " + \
               f"tradID: {self.traderID}, " + \
               f"side:{self.side}, " + \
               f"price:{self.price}, " + \
               f"qty:{self.qty}, " + \
               f"ts:{self.ts}]"

    def log_order_add(self):
        logging.info(f"[orderAdd, " + \
                     f"tradID: {self.traderID}, " + \
                     f"side:{self.side}, " + \
                     f"price:{self.price}, " + \
                     f"qty:{self.qty}, " + \
                     f"ts:{self.ts}]")

class OrderCancel():
    """
    If trader wants to decrease qautnity of trade or cancel trade,
    they instantiate this class.
    """
    def __init__(self, ord, qty):
        """
        Parameters
        ----------
        ord (OrderAknowledgement instance):
            randomly chosen order from trader.live_orders to cancel or decrease
        qty (int): randomly chosen qty from 0 to
        """
        self.orderID = ord.orderID
        self.qty = qty
        self.ts = datetime.now()

        self._log_order_cancel()

    def __repr__(self):
        return f"[orderCancel, " + \
               f"orderID: {self.orderID}, " + \
               f"qty:{self.qty} "

    def _log_order_cancel(self):
        logging.info(f"[orderCancel, " + \
                     f"orderID: {self.orderID}, " + \
                     f"qty:{self.qty},  " + \
                     f"ts:{self.ts}]")


class OrderAknowledgement(OrderAdd):
    _N = count(1)
    def __init__(self, traderID, side, price, qty):
        super().__init__(traderID, side, price, qty)
        self.orderID = 'order' + str(next(self._N))
        self.ts = datetime.now()


    def __repr__(self):
        return str(self.qty)

    def log_order_aknowledgement(self):
        logging.info(f"[orderAknowledgement, " + \
                     f"orderId: {self.orderID}, " + \
                     f"tradID: {self.traderID}, " + \
                     f"side:{self.side}, " + \
                     f"price:{self.price}, " + \
                     f"qty:{self.qty}, " + \
                     f"ts:{self.ts}]")

    def print_whole_order(self):
        return f"[orderAknowledgement, " + \
                         f"orderId: {self.orderID}, " + \
                         f"tradID: {self.traderID}, " + \
                         f"side:{self.side}, " + \
                         f"price:{self.price}, " + \
                         f"qty:{self.qty}, " + \
                         f"ts:{self.ts}]"

class Fill():
    _N = count(1)
    def __init__(self, order, qty):
        self.fillId = 'fill' + str(next(self._N))
        self.orderID = order.orderID
        self.traderID = order.traderID
        self.side = order.side
        self.qty = qty
        self.ts = datetime.now()


    def __repr__(self):
        return f"[fill, " + \
             f"fillId: {self.fillId}, " + \
             f"traderID: {self.traderID}, " + \
             f"orderId: {self.orderID}, " + \
             f"qty:{self.qty}, " + \
             f"side:{self.side}, " + \
             f"ts:{self.ts}]"

    def _log_order_fill(self):
        logging.info(f"[fill, " + \
                     f"fillId: {self.fillId}, " + \
                     f"traderID: {self.traderID}, " + \
                     f"orderId: {self.orderID}, " + \
                     f"qty:{self.qty}, " + \
                     f"side:{self.side}, " + \
                     f"ts:{self.ts}]")




if __name__=="__main__":
    ordAk = OrderAdd('traderid1')
    print(ordAk)
    print(OrderAknowledgement(ordAk))
