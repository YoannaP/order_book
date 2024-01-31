from collections import defaultdict

from classes.messages import *

class Exchange:
    def __init__(self):
        self.buys = defaultdict(list)
        self.sells = defaultdict(list)
        self.ak_orders = []
        self.fillsFromOrder = []

    def aknowledgeOrder(self, orderAdd):
        """
        Aknowledges that order is received by exchange.

        Parameters
        ----------
        orderAdd (orderAdd object)
        """
        ord_ak = OrderAknowledgement(traderID=orderAdd.traderID,
                                     side=orderAdd.side,
                                     price=orderAdd.price,
                                     qty=orderAdd.qty)

        self.ak_orders.append(ord_ak)
        ord_ak.log_order_aknowledgement()

        return ord_ak

    def processOrder(self, type, order):
        """
        Refreshes fills, given new order, processes new order
        and logs the fills after the order.

        Parameters
        ----------
        type (str): add or cancel
        order (orderAknowledgement object): order to process
        """
        self.fillsFromOrder = []
        if type=='add':
            self._processOrderAdd(order)
        else:
            self._processOrderCancel(order)

        self._logFills()


    def _processOrderAdd(self, aknowledged_order):
        """
        Processes latest order in market. If can match - enters into matching
        loop. Otherwise, it is added in the order book of buys/sells.

        Parameters
        ----------
        aknowledged_order (aknowledgedOrder object): order to process
        """

        currentPrice = aknowledged_order.price
        currentSide = aknowledged_order.side
        currentQty = aknowledged_order.qty

        if currentSide==-1:
            max_buy = self._max_buy()
            if currentPrice <= max_buy and self.buys:
                self._match_orders(order=aknowledged_order, min_max=max_buy)
            else:
                self.sells[currentPrice].append(aknowledged_order)
        else:
            min_sell = self._min_sell()
            if currentPrice >= min_sell and self.sells:
                self._match_orders(order=aknowledged_order, min_max=min_sell)
            else:
                self.buys[currentPrice].append(aknowledged_order)

        return

    def _match_orders(self, order, min_max):
        """
        Matches appropriate orders in order book.

        Parameters
        ----------
        order (orderAknowledgement object): order which needs to be matched with
            the best order
        min_max (int): either min or max order price to match order with
        """
        currentPrice = order.price
        currentSide = order.side
        currentQty = order.qty

        if currentSide==1:
            min_sell = min_max

            if len(self.sells[min_sell])!=0:
                minSellQty = self.sells[min_sell][0].qty
            else:
                self.sells[currentPrice].append(order)
                return

            tradeSize = min(minSellQty, currentQty)
            currentQty -= tradeSize
            minSellQty -= tradeSize

            self.sells[min_sell][0].qty = minSellQty
            filledOrder = self.sells[min_sell][0]
            if minSellQty==0:
                filledOrder = self.sells[min_sell].pop(0)
                order.qty = currentQty
                self._create_fill_and_send(filledOrder, order, tradeSize)
                if len(self.sells[min_sell])==0:
                    del self.sells[min_sell]

        else:
            max_buy = min_max
            if len(self.buys[max_buy])!=0:
                maxBuyQty = self.buys[max_buy][0].qty
            else:
                self.sells[currentPrice].append(order)
                return

            tradeSize = min(maxBuyQty, currentQty)
            currentQty -= tradeSize
            maxBuyQty -= tradeSize

            self.buys[max_buy][0].qty = maxBuyQty
            filledOrder = self.buys[max_buy][0]

            if maxBuyQty==0:
                filledOrder = self.buys[max_buy].pop(0)
                order.qty = currentQty
                self._create_fill_and_send(filledOrder, order, tradeSize)
                if len(self.buys[max_buy])==0:
                    del self.buys[max_buy]

        if currentQty!=0:
            self._processOrderAdd(order)
        else:

            self._create_fill_and_send(filledOrder, order, tradeSize)
            return

    def _logFills(self):
        """
        After current trade is completed in exchange, all the logs are recorded.
        """
        for fill in self.fillsFromOrder:
            fill._log_order_fill()

    def _create_fill_and_send(self, o2, o1, tradeQty):
        """
        Creates a fill message and adds it to fills for matched orders o1, o2
        Keeps a record of unique fill ids so can add qty to order which has been
        partially filled in current trade.

        Parameters
        ----------
        o2 (orderAknowledgement object)
        o1 (orderAknowledgement object)
        tradeQty (int): how much the match was for
        """

        if len(self.fillsFromOrder)==0:
            fill_1 = Fill(order=o1,
                          qty=tradeQty)
            self.fillsFromOrder.append(fill_1)
        else:
            for fill in self.fillsFromOrder:
                if fill.orderID==o1.orderID:
                    fill.qty += tradeQty

        fill_2 = Fill(order=o2,
                      qty=tradeQty)
        self.fillsFromOrder.append(fill_2)

        return

    def _processOrderCancel(self, order):
        """
        Replaces or removes the order from order book.

        Parameters
        ----------
        order (orderAknowledgement object): order to cancel qty from.
        """
        # find order to replace
        ordToReplace = next((ord for ord in self.ak_orders if ord.orderID==order.orderID), ord)

        # replace quantity order which will be used to replace
        ordToReplace.qty=ordToReplace.qty - order.qty


        if ordToReplace.side==1:
            for i, each_buy in enumerate(self.buys[ordToReplace.price]):
                if each_buy.orderID==order.orderID:
                    each_buy = ordToReplace
                    if each_buy.qty==0:
                        self.buys[ordToReplace.price].pop(i)
                    break
        else:
            for i, each_sell in enumerate(self.sells[ordToReplace.price]):
                if each_sell.orderID==order.orderID:
                    each_sell = ordToReplace
                    if each_sell.qty==0:
                        self.sells[ordToReplace.price].pop(i)
                    break

        order.qty = ordToReplace.qty

    def _min_sell(self):
        """
        Gets the minimum sell price of order book.

        Returns
        -------
        (int): minimum sell price
        """
        if self.sells:
            return min(self.sells.keys())
        return 100000

    def _max_buy(self):
        """
        Gets maximum buy price of order book.

        Returns
        -------
        (int): maximum buy price
        """
        if self.buys:
            return max(self.buys.keys())
        return 0


if __name__=="__main__":
    ex = Exchange()
