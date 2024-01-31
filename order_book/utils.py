import random


def generate_order_params(base_price=50.34, delta_price=10, max_qty=50):
    """
    Generates random side, price, qty for an add_order

    Parameters
    ----------
    base_price (float): the closing price of stock
    delta_price (float): the price increment of the stock
    max_qty (int):
    """

    random_price = round(base_price + delta_price * random.uniform(-1, 1), 2)
    random_qty = random.randint(1, max_qty)

    random_side = random.choice([-1, 1])

    return random_side, random_price, random_qty
