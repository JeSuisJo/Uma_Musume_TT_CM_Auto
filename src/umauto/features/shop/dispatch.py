"""Pick a buying strategy from config, or dismiss the shop when off."""

import time

from ... import screen
from .buy_all import buy_all_sales
from .buy_specific import buy_specific_sales
from .mode import shop_mode


def buy_sales():
    """Buy per the configured mode; return True if a purchase flow ran.

    ``"all"``/``"specific"`` open the shop, buy and go home, returning True.
    ``"off"`` touches nothing and returns False, leaving the caller to dismiss
    the shop prompt however it needs to.
    """
    mode = shop_mode()
    if mode == "all":
        buy_all_sales()
        return True
    if mode == "specific":
        buy_specific_sales()
        return True
    return False


def handle_daily_sales():
    """When the shop prompt is showing in a daily mode, buy or dismiss it.

    Detects the shop itself, so callers can invoke it unconditionally: if no
    shop prompt is on screen it does nothing.
    """
    if not screen.see("shop"):
        return

    if not buy_sales():
        screen.tap("shop_cancel")
        time.sleep(1)
        screen.tap("home")
