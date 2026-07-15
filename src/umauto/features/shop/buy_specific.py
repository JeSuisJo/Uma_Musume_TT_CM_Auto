"""Buy only the configured ``shop_items`` (the ``"specific"`` mode).

Opens the shop and searches the scrollable item list for each configured item's
icon template, tapping every copy found (an item listed twice is bought twice),
then confirms the basket once at the end.
"""

import time

from ... import screen
from ...config import config
from ...coords import coords
from ...driver import driver
from .shop_items import COORD_BY_NAME

# Safety cap on how many times to scroll the shop list while hunting items.
_MAX_SCROLLS = 6

# Template-match confidence for locating a shop item's icon in the list.
_ITEM_THRESHOLD = 0.9
# Colour-resemblance gate: rejects greyed-out (already-selected) icons that the
# brightness-invariant template match would otherwise still find. Raise it if
# selected items get re-detected, lower it if available items get skipped.
_ITEM_COLOR_THRESHOLD = 0.85

# Seconds to wait before buying the items visible in the list. Raise it if
# items get tapped at the wrong spot.
_DELAY = 0.8


def buy_specific_sales():
    """Buy only the items listed in the ``shop_items`` config, then go home.

    Opens the shop and searches the item list for each configured item's icon
    template. Any icon found in the current view is selected (its row buy button
    is tapped, at a fixed X offset from the icon -- see ``shop_buy_offset``);
    then the list is scrolled and searched again, ``_MAX_SCROLLS`` times. Items
    are re-checked on every pass so duplicates (e.g. two Star Pieces at
    different spots) are all bought. The basket is confirmed once at the end.
    """
    screen.tap("shop")
    screen.wait("in_shop")
    print("In the shop")
    time.sleep(1)

    targets = [n for n in config.get("shop_items", []) if n in COORD_BY_NAME]
    for name in config.get("shop_items", []):
        if name not in COORD_BY_NAME:
            print(f"  Unknown shop item '{name}', skipping")

    # Each pass checks every configured item in the current view first; only
    # then does it scroll (and never after the last pass).
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
    """Return True if the pixel at ``name``'s ``region`` point matches its ``rgb``.

    These entries store a single ``[x, y]`` point under ``region`` (not ``tap``)
    plus an ``rgb`` target, so this reads the live pixel there and compares it.
    """
    block = coords(name)
    x, y = block["region"]
    return driver.is_color(x, y, block["rgb"], tolerance)


def _buy_visible(targets):
    """Select every configured item currently on screen; return how many.

    Items are never marked done, so the same name is re-checked on each pass:
    a shop that lists an item twice gets it bought each time it comes into view.

    Every item is located against one frozen capture before anything is tapped,
    so the whole view costs a single screenshot instead of one per item.
    """
    off = coords("shop_buy_offset")
    # Let the list settle before the capture: the taps below aim at coordinates
    # read from that one frame, so it must show the view at rest. Waiting after
    # the capture instead would only make those coordinates staler.
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
    """Confirm and close the shop once every wanted item has been selected."""
    screen.wait("shop_confirm")
    screen.tap("shop_confirm")
    time.sleep(1.5)
    screen.wait("shop_buy")
    screen.tap("shop_buy")
    time.sleep(1.5)
    screen.wait("shop_close_1")
    screen.tap("shop_close_1")
    time.sleep(1)
