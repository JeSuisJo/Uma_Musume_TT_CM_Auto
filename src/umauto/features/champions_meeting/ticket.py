"""Collect the free daily Champions Meeting ticket."""

import time

from ... import screen


def collect_ticket():
    screen.tap("ticket")
    time.sleep(2)
    if screen.see_template("no_ticket_cm"):
        print("Tickets already collected")
    else:
        screen.tap("ticket_collect")
        time.sleep(1)
        screen.tap("ticket_close")
        time.sleep(1)
    screen.tap("back_to_cm")
    time.sleep(1.5)
