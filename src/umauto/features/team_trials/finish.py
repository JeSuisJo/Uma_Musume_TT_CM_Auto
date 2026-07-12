"""Handle post-race popups, optional shopping, and return to the trial menu."""

import time

from ... import screen
from ..shop import buy_sales

_POPUPS = ("highscore", "story_unlocked", "next_go_to_reward", "next_reward")


def finish_run():
    shopped = False

    while not screen.see("finish_run"):
        for popup in _POPUPS:
            if screen.see(popup):
                time.sleep(0.5)
                screen.tap(popup)

        if screen.see("shop"):
            time.sleep(0.5)
            if buy_sales():
                shopped = True
                break
            screen.tap("shop_cancel")
            time.sleep(1)

    if shopped:
        return

    print("Go back to the trial menu")
    time.sleep(0.8)
    screen.tap("finish_run")
