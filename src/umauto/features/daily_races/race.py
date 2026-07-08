import time

from ... import screen
from ..common import handle_daily_sales


def race():
    screen.wait("daily_race_close")
    screen.tap("daily_race_close")
    time.sleep(2.5)
    if screen.see("shop"):
        time.sleep(0.5)
        handle_daily_sales()
    screen.tap("home")
