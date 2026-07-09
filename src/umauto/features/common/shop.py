"""Shared shop handling: buy all daily-sale items across every mode."""

import time

from ... import screen
from ...config import config


def buy_all_sales(then=None):
    """Buy every daily-sale item, then run ``then`` (defaults to going home).

    ``then`` lets callers return somewhere other than the home screen once the
    purchase is done (Team Trials goes back to the trial menu, for example).
    """
    screen.tap("shop")
    screen.wait("in_shop")

    time.sleep(1)
    screen.tap("buy_all")
    time.sleep(2)
    screen.tap("shop_buy")
    time.sleep(2)
    screen.tap("shop_confirm")
    time.sleep(2)
    screen.tap("shop_close_1")
    time.sleep(2)
    if then is not None:
        then()
    else:
        screen.tap("home")


def handle_daily_sales():
    """When the shop prompt is showing in a daily mode, buy or dismiss it.

    Detects the shop itself, so callers can invoke it unconditionally: if no
    shop prompt is on screen it does nothing.
    """
    if not screen.see("shop"):
        return

    if config.get("daily_sales_buy"):
        buy_all_sales()
    else:
        screen.tap("shop_cancel")
        time.sleep(1)
        screen.tap("home")
