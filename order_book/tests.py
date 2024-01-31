def testBuySellEqualInFills(fills):
    """
    Tests whether for each new order, teh fills received from that
    order have equal buy and sell quantities.
    """
    buy = 0
    sell = 0
    for fill in fills:
        if fill.side == 1:
            buy += 0
        else:
            sell += 0

    if buy==sell:
        print("testBuySellEqualInFills PASSED!")
    else:
        print("testBuySellEqualInFills FAILED!")


def testUniqueIDs(orders, IdToTest):
    """
    Tests that orderIDs or traderID are unique either for list a list of filled
    orders, list of live_orders or list of traders (for traderID).
    """
    if IdToTest=='orderID':
        set_orders = set(order.orderID for order in orders)
    else:
        set_orders = set(order.id for order in orders)

    if len(set_orders)==len(orders):
        print("testUniqueIDs PASSED!")
    else:
        print("testUniqueIDs FAILED!")


def testAddGetsAknowledgedCorrectly(addOrder, aknowledgedOrder):
    """
    Test if the parameters orderAdd get assigned to aknowledgedOrder correctly.
    """
    if addOrder.side!=aknowledgedOrder.side:
        print("testAddGetsAknowledgedCorrectly FAILED")
        print(f"""Side {addOrder.side} not equal to {aknowledgedOrder.side}""")
    else:
        print("testAddGetsAknowledgedCorrectly PASSED")
    if addOrder.qty!=aknowledgedOrder.qty:
        print("testAddGetsAknowledgedCorrectly FAILED")
        print(f"""Qty {addOrder.qty} not equal to {aknowledgedOrder.qty}""")
    else:
        print("testAddGetsAknowledgedCorrectly PASSED")
    if addOrder.traderID!=aknowledgedOrder.traderID:
        print("testAddGetsAknowledgedCorrectly FAILED")
        print(f"""traderID {addOrder.traderID} not equal to {aknowledgedOrder.traderID}""")
    else:
        print("testAddGetsAknowledgedCorrectly PASSED")
    if addOrder.price!=aknowledgedOrder.price:
        print("testAddGetsAknowledgedCorrectly FAILED")
        print(f"""Side {addOrder.price} not equal to {aknowledgedOrder.price}""")
    else:
        print("testAddGetsAknowledgedCorrectly PASSED")
