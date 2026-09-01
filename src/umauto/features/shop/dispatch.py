import time

from ... import screen
from .buy_all import buy_all_sales
from .buy_specific import buy_specific_sales
from .mode import shop_mode


def buy_sales():
    mode = shop_mode()
    if mode == "all":
        buy_all_sales()
        return True
    if mode == "specific":
        buy_specific_sales()
        return True
    return False


def handle_daily_sales():
    if not screen.see("shop"):
        return False

    if not buy_sales():
        screen.tap("shop_cancel")
        time.sleep(1)
        screen.tap("home")
    return True
