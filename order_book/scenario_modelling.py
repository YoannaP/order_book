import logging

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(filename='logging.log', format=FORMAT, level=logging.DEBUG)

from classes.messages import *
from classes.exchange import *
from classes.trader import *
from utils import *
from tests import *

from pprint import pprint
import time

if __name__=='__main__':

    number_of_traders = 10
    traders = [Trader() for i in range(number_of_traders)]
    exchange=Exchange()

    #random.seed(22)
    t_end = time.time() + 60 * 1
    while time.time() < t_end:
        trader = random.choice(traders)
        order_choice = random.choice(['add', 'cancel'])

        if order_choice=='add' or not trader.live_orders:
            params =  generate_order_params()
            order = trader.sendOrderAdd(side=params[0],
                                        price=params[1],
                                        qty=params[2])
            aknowledged_order = exchange.aknowledgeOrder(order)
            trader.receiveAknowledgement(aknowledged_order)
            exchange.processOrder(type='add', order=aknowledged_order)

        elif order_choice=='cancel':
            order_to_cancel = random.choice(trader.live_orders)
            order=trader.sendOrderCancel(ord=order_to_cancel,
                                         qty=random.randint(1, order_to_cancel.qty))
            exchange.processOrder(type='cancel', order=order)


        for trader in traders:
            trader.updateLiveOrders()
    print(exchange.sells)
    print(exchange.buys)
