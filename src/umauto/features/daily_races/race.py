"""Close the race result, handle the shop prompt, and return home."""

import time

from ... import screen
from ..shop import handle_daily_sales


def collect_rewards():
    screen.wait("daily_race_close")
    screen.tap("daily_race_close")
    time.sleep(2.5)
    handle_daily_sales()
    screen.tap("home")
