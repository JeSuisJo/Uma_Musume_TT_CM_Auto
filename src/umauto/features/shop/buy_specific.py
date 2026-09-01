import time

from ... import screen
from ...config import config
from ...coords import coords
from ...driver import driver
from .shop_items import COORD_BY_NAME

_MAX_SCROLLS = 6

_ITEM_THRESHOLD = 0.9
_ITEM_COLOR_THRESHOLD = 0.85

_DELAY = 0.8


def buy_specific_sales():
    screen.tap("shop")
    screen.wait("in_shop")
    print("In the shop")
    time.sleep(1)

    targets = [n for n in config.get("shop_items", []) if n in COORD_BY_NAME]
    for name in config.get("shop_items", []):
        if name not in COORD_BY_NAME:
            print(f"  Unknown shop item '{name}', skipping")

    for pass_i in range(_MAX_SCROLLS + 1):
        _buy_visible(targets)
        if pass_i < _MAX_SCROLLS:
            with driver.frozen():
                done = _color_at("shop_already_buy") and not _color_at(
                    "shop_buy_but_not_finish"
                )
            if done:
                break
            time.sleep(0.6)
            screen.drag_hold_to("shop_scroll")
            time.sleep(0.6)

    _confirm_purchase()

    time.sleep(1.5)
    screen.tap("home")


def _color_at(name, tolerance=10):
    block = coords(name)
    x, y = block["region"]
    return driver.is_color(x, y, block["rgb"], tolerance)


def _buy_visible(targets):
    off = coords("shop_buy_offset")
    time.sleep(_DELAY)
    with driver.frozen():
        found = [
            loc
            for name in targets
            for loc in screen.find_all(
                COORD_BY_NAME[name],
                threshold=_ITEM_THRESHOLD,
                color_threshold=_ITEM_COLOR_THRESHOLD,
            )
        ]

    for loc in found:
        driver.tap(loc[0] + off["dx"], loc[1] + off["dy"])
        time.sleep(0.8)
    return len(found)


def _confirm_purchase():
    screen.wait("shop_confirm")
    screen.tap("shop_confirm")
    time.sleep(1.5)
    screen.wait("shop_buy")
    screen.tap("shop_buy")
    time.sleep(1.5)
    screen.wait("shop_close_1")
    screen.tap("shop_close_1")
    time.sleep(1)
