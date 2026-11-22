import time

from ... import screen
from ...config import config

_STEPS = (
    "no_rp_close",
    "home",
    "menu_button",
    "inventory_button",
    "carrot_use",
    "carrot_max",
    "carrot_ok",
    "carrot_close",
)


def refill_rp():
    """Home -> Menu -> Inventory -> Carrot Jelly Mini -> Use -> Max -> OK. Returns True if attempted."""
    if not config.get("use_carrot_jelly_TT"):
        return False
    print("Using Carrot Jelly Mini")
    for step in _STEPS:
        screen.tap(step)
        time.sleep(1)
    screen.tap("home")
    time.sleep(1)
    return True
