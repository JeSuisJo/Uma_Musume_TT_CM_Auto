"""Buy every daily-sale item in one tap (the ``"all"`` mode)."""

import time

from ... import screen


def buy_all_sales():
    """Buy every daily-sale item, then go home."""
    screen.tap("shop")
    screen.wait("in_shop")
    print("In the shop")

    time.sleep(1)
    screen.tap("buy_all")
    time.sleep(2)
    screen.tap("shop_confirm")
    time.sleep(2)
    screen.tap("shop_buy")
    time.sleep(2)
    screen.tap("shop_close_1")
    time.sleep(2)
    screen.tap("home")
