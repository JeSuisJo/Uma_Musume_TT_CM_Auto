"""Shared shop handling: buy all daily-sale items across every mode."""

import time

from ... import screen
from ...config import config


def buy_all_sales():
    """Buy every daily-sale item"""
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
    screen.tap("home")


def handle_daily_sales():
    """On the shop prompt of a daily mode, buy or dismiss per the config."""
    if config.get("daily_sales_buy"):
        buy_all_sales()
    else:
        screen.tap("shop_cancel")
        time.sleep(1)
        screen.tap("home")
