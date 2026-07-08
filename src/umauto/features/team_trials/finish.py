"""Handle post-race popups, optional shopping, and return to the trial menu."""

import time

from ... import screen
from ...config import config
from ..common import buy_all_sales

_POPUPS = ("highscore", "story_unlocked", "next_go_to_reward", "next_reward")


def _back_to_trial_menu():
    screen.wait("tt_button")
    screen.tap("tt_button")


def finish_run():
    shopped = False

    while not screen.see("finish_run"):
        for popup in _POPUPS:
            if screen.see(popup):
                time.sleep(0.5)
                screen.tap(popup)

        if screen.see("shop"):
            time.sleep(0.5)
            if config.get("daily_sales_buy"):
                buy_all_sales(then=_back_to_trial_menu)
                shopped = True
                break
            screen.tap("shop_cancel")
            time.sleep(1)

    if shopped:
        return

    print("Go back to the trial menu")
    time.sleep(0.8)
    screen.tap("finish_run")
