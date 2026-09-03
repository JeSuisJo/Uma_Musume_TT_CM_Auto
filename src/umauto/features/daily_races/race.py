import time

from ... import screen
from ..popups import dismiss_uma_outing
from ..shop import handle_daily_sales


def collect_rewards():
    screen.wait("daily_race_close")
    screen.tap("daily_race_close")
    time.sleep(2.5)
    dismiss_uma_outing()
    handle_daily_sales()
    screen.tap("home")
